import traceback
import re
import requests

class EventWebhooks:
    class HookAction():
        def __init__(self, url = 'localhost', json = None, headers = 'Content-Type: application/json'):
            self.url = url
            self.json = json

        def invoke(self):
            requests.post(self.url, json = self.json)

    class RegexWebhook():
        def __init__(self, name = None, sensor_name_match = None, sensor_content_match = None,
                        hook = None):
            self.name = name
            self.sensor_name_match = sensor_name_match
            self.sensor_content_match = None
            self.hook = hook

        def run_match_action(self, message):
            match = False
            if self.sensor_name_match and 'sensorEvents' in message:
                sensor_events = message['sensorEvents']
                if self.sensor_name_match:
                    for key in self.sensor_name_match.keys():
                        if key in sensor_events and \
                                self.sensor_name_match[key] in sensor_events[key]:
                            if self.sensor_content_match:
                                events = sensor_events[key][self.sensor_name_match[key]]
                                for event in events:
                                    for key in self.sensor_content_match:
                                        if key in event:
                                            if len(re.findall(self.sensor_content_match[key],
                                                      str(event[key]))):
                                                match = True
                            else:
                                match = True
            if match and self.hook:
                self.hook.invoke()

    def __init__(self) -> None:
        self.webhooks = []
        self.webhooks.append(EventWebhooks.RegexWebhook(
            name = "SignalOn",
            sensor_name_match =
            {
                "presenceSensor" : "D4146053-308A-47F5-809A-4244AA86F6B9"
            }
            sensor_content_match =
            {
                "updateCount" : 1
            }
            hook =
            EventWebhooks.HookAction(
                url="ntcip-relay-server",
                json={
                    "phase_control_group" : 1,
                    "phase" : 1,
                    "signal_type" : True,
                    "mib" : "1.3.6.1.4.1.1206.4.2.1.1.5.1.7"
                })
        ))
        self.webhooks.append(EventWebhooks.RegexWebhook(
            name = "SignalOff",
            sensor_name_match =
            {
                "presenceSensor" : "D4146053-308A-47F5-809A-4244AA86F6B9"
            }
            sensor_content_match =
            {
                "endedAt" : ".*"
            }
            hook = EventWebhooks.HookAction(
                url="ntcip-relay-server",
                json={
                    "phase_control_group" : 1,
                    "phase" : 1,
                    "signal_type" : False,
                    "mib" : "1.3.6.1.4.1.1206.4.2.1.1.5.1.7"
                })
        ))


    def callback(self, message):
        for wh in self.webhooks:
            try:
                wh.run_match_action(message)
            except Exception as e:
                print(f"Caught exception {e} handling {wh.name} webhook")
                traceback.print_exc()
