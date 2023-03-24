import traceback
import re
import requests
import logging
import json
import threading

class EventWebhooks:
    class HookAction():
        def __init__(self, url = 'http://localhost', json = None, headers = 'Content-Type: application/json'):
            self.url = url
            self.json = json

        def invoke(self):
            r = requests.post(self.url, json = self.json)
            r.raise_for_status()
            logging.info(f"POST request complete for {self.json} on {self.url} with response {r}")


    class RegexWebhook():
        def __init__(self, name = None, sensor_name_match = None, sensor_content_match = None,
                        hook = None):
            self.name = name
            self.sensor_name_match = sensor_name_match
            self.sensor_content_match = sensor_content_match
            self.hook = hook
            self.sensor_events = 0
            self.sensor_name_events = 0
            self.hook_invocations = 0

        def run_match_action(self, message):
            match = False
            if self.sensor_name_match and 'sensorEvents' in message:
                sensor_events = message['sensorEvents']
                self.sensor_events = self.sensor_events+1
                if self.sensor_name_match:
                    for key in self.sensor_name_match.keys():
                        self.sensor_name_events = self.sensor_name_events+1
                        if key in sensor_events and \
                                self.sensor_name_match[key] in sensor_events[key]:
                            if self.sensor_content_match:
                                events = sensor_events[key][self.sensor_name_match[key]]
                                for event in events:
                                    for key in self.sensor_content_match:
                                        if key in event:
                                            regex_str = self.sensor_content_match[key]
                                            if not isinstance(regex_str, str):
                                                # Handle ints by looking for exact match
                                                regex_str = f"^{regex_str}$"
                                            if len(re.findall(re.compile(regex_str),
                                                      str(event[key]))):
                                                match = True
                            else:
                                match = True
            if match and self.hook:
                self.hook.invoke()
                self.hook_invocations = self.hook_invocations + 1

    def __init__(self) -> None:
        self.webhooks = []
        self.callback_count = 0
        self.webhooks.append(EventWebhooks.RegexWebhook(
            name = "SignalOn",
            sensor_name_match = {
                "presenceSensor" : "D4146053-308A-47F5-809A-4244AA86F6B9"
            },
            sensor_content_match ={
                "updateCount" : 1
            },
            hook = EventWebhooks.HookAction(
                url="http://ntcip-relay-server:8080/pedcall/",
                json={
                    "phase_control_group" : 1,
                    "phase" : 1,
                    "activate" : True,
                    "mib" : "1.3.6.1.4.1.1206.4.2.1.1.5.1.7"
                })
        ))
        self.webhooks.append(EventWebhooks.RegexWebhook(
            name = "SignalOff",
            sensor_name_match = {
                "presenceSensor" : "D4146053-308A-47F5-809A-4244AA86F6B9"
            },
            sensor_content_match = {
                "endedAt" : ".*"
            },
            hook = EventWebhooks.HookAction(
                url="http://ntcip-relay-server:8080/pedcall/",
                json={
                    "phase_control_group" : 1,
                    "phase" : 1,
                    "activate" : False,
                    "mib" : "1.3.6.1.4.1.1206.4.2.1.1.5.1.7"
                })
        ))
        threading.Timer(10, self.print_status).start()

    def print_status(self):
        sensor_matches = {}
        for wh in self.webhooks:
            sensor_matches[wh.name] = { 'sensor_events' : wh.sensor_events,
                                        'sensor_name_events' : wh.sensor_name_events,
                                        'hook_invocations': wh.hook_invocations
            }
        logging.info(f"{self.callback_count} callbacks: {json.dumps(sensor_matches, indent=4, sort_keys=True)}")
        threading.Timer(10, self.print_status).start()


    def callback(self, message):
        self.callback_count = self.callback_count+1
        for wh in self.webhooks:
            try:
                wh.run_match_action(message)
            except Exception as e:
                logging.error(f"Caught exception {e} handling {wh.name} webhook")
                traceback.print_exc()
