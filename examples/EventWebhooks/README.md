# Event Webhooks Example

This example demonstrates event webhooks invocation in response to
corresponding events from the SIO pipeline.

## Quickstart

```bash
docker-compose up
```

## Configuration

See the [config/config.json](config/config.json) for an example webhook configuration
which invokes webhook POST methods on a URL endpoint in response to a matching event

| Field             | Example Value         | Description    |
| --------------    | --------------------- | -------------- |
| regex_webhooks    | See description below | Array of regex and webhook dictionaries |
| name              | "SensorOn"            | A customizable name of the sensor (for logging purposes) |
| sensor_name_match | "presenceSensor" : "D4146053-308A-47F5-809A-4244AA86F6B9" | Dictionary describing the type of sensor and label for the specific sensor to match with this event |
| sensor_content_match | "updateCount" : 1 | Regex content match for fields within the sensor described by `sensor_name_match` which provides a further match on this sensor.  Specify a string to be treated as a regex.  Specify an integer value to exactly match this integer value.  The "updateCount" : 1 value for a region sensor means the beginning activation for
a region based sensor event. |
| hooks | [ {"url" : "http://myserver:8080/myhook/", "json" : { "myvalue": 1 } } ] | Array of dictionary containing webhooks to invoke on `sensor_name_match` and `sensor_content_match`. Must include keys "url" to use with a POST request and "json" to include in the json content of the request |

## Debugging in VSCode

1. Install [Docker Extension for VSCode](https://marketplace.visualstudio.com/items?itemName=ms-azuretools.vscode-docker)
2. Right click on [docker-compose-debug.yml](docker-compose-debug.yml) and
select "Docker Compose Up"
4. Add this snippet to your `.vscode/launch.json`
```
{
    // Use IntelliSense to learn about possible attributes.
    // Hover to view descriptions of existing attributes.
    // For more information, visit: https://go.microsoft.com/fwlink/?linkid=830387
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Python: Remote Attach Event Webhooks",
            "type": "python",
            "request": "attach",
            "connect": {
                "host": "localhost",
                "port": 5678
            },
            "pathMappings": [
                {
                    "localRoot": "${workspaceFolder}/examples/lib",
                    "remoteRoot": "/usr/src/lib"
                },
                {
                    "localRoot": "${workspaceFolder}/examples/EventWebhooks/src",
                    "remoteRoot": "/usr/src/app"
                }
            ],
            "justMyCode": true
        }
    ]
}
```
5. Click the "Debug" option in visual studio code and select "Python: Remote Attach Event Webhooks".
