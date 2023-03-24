import traceback
import re
import requests
import logging
import json
import threading

class EventWebhooks:
    class HookAction():
        def __init__(self, dict):
            self.url = dict.get('url',None)
            self.json = dict.get('json', None)

        def invoke(self):
            r = requests.post(self.url, json = self.json)
            r.raise_for_status()
            return r


    class RegexWebhook():
        def __init__(self, dict):
            self.name = dict.get('name', "NoName")
            self.sensor_name_match = dict.get('sensor_name_match', None)
            self.sensor_content_match = dict.get('sensor_content_match', None)
            self.hooks = dict.get('hooks', None)
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
            if match and self.hooks:
                for hook in self.hooks:
                    try:
                        r = hook.invoke()
                        self.hook_invocations = self.hook_invocations + 1
                        logging.info(f"hook complete for {self.name} on {hook.url} with payload {hook.json} and response {r}")
                    except Exception as e:
                        logging.exception(f"hook for {self.name} failed with exception")

    def __init__(self, config_file) -> None:
        self.webhooks = []
        self.callback_count = 0
        with open(config_file) as json_file:
            data = json.load(json_file)
            if 'regex_webhooks' in data:
                for webhook in data['regex_webhooks']:
                    hook = None
                    logging.info(f"Setting up webhook {webhook} based on configuration")
                    if 'hooks' in webhook:
                        hooks = []
                        for hook in webhook['hooks']:
                            hooks.append(EventWebhooks.HookAction(hook))
                        webhook['hooks'] = hooks
                    self.webhooks.append(EventWebhooks.RegexWebhook(webhook))
        threading.Timer(10, self.print_status).start()

    def print_status(self):
        sensor_matches = {}
        for wh in self.webhooks:
            sensor_matches[wh.name] = { 'sensor_events' : wh.sensor_events,
                                        'sensor_name_events' : wh.sensor_name_events,
                                        'hook_invocations': wh.hook_invocations
            }
        logging.info(f"Processed {self.callback_count} callbacks with hook status: {sensor_matches}")
        threading.Timer(10, self.print_status).start()


    def callback(self, message):
        self.callback_count = self.callback_count+1
        for wh in self.webhooks:
            try:
                wh.run_match_action(message)
            except Exception as e:
                logging.exception(f"Caught exception handling {wh.name} webhook")
                traceback.print_exc()
