# CloudLog
Logs agregation system built on top of AWS

## Logs mapping

### Log format
* `os`: string - [Windows,Linux]
* `severity`: number
* `message`: string
* `timestamp`: number
* `hostname`: string - workstation name
* `unit`: string - process/application
* `type`: string - [System, Application, CloudLogger]
* `raw`: string - raw format of log


### OS logs mapping
| field     | Windows       | Linux                                                    |
| --------- | ------------- | -------------------------------------------------------- |
| os        | "Windows"     | "Linux"                                                  |
| severity  | Level         | PRIORITY                                                 |
| message   | Message       | MESSAGE                                                  |
| timestamp | TimeCreated   | __REALTIME_TIMESTAMP                                     |
| hostname  | MachineName   | _HOSTNAME                                                |
| unit      | ProviderName  | _EXE                                                     |
| type      | ContainerName | `Application` if ("opt" or "snap") in _EXE else `System` |
| raw       | *             | *                                                        |

## AWS

### API
defined in [swagger definition](./infra/openapi/cloudlog_api.yaml)



### Database
Database build on AWS DynamoDB

#### Schema

| field     | type   | constraints                      | example                               |
| --------- | ------ | -------------------------------- | ------------------------------------- |
| id        | string | uuid                             | *f43t446yg*                           |
| os        | string | (Linux, Windows)                 | *Linux*                               |
| severity  | number | 0 < 7                            | *3*                                   |
| message   | string | ---                              | *unable to update icon for discord1*  |
| timestamp | number | unix timestamp                   | *1675557738587889*                    |
| hostname  | string | ---                              | *szymon-latitude*                     |
| unit      | string | ---                              | */snap/postman/184/usr/share/postman* |
| type      | string | (Application,System,CloudLogger) | *Application*                         |
| raw       | string | *                                | *raw log fetched from system*         |