# Event Webhooks Example

This example demonstrates event webhooks invocation in response to
corresponding events from the SIO pipeline.

## Quickstart

```bash
docker-compose up
```

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
