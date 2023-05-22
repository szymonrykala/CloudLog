# AWS Infrastructure

## Database
Built on DynamoDB database.

### Schema
All constraints has been created programatically - they are forced by service that writes t database - [save_logs lambda](../lambda/save_logs/)
| field     | type   | constraints                      | example                               |
| --------- | ------ | -------------------------------- | ------------------------------------- |
| id        | string | uuid                             | *f43t446yg*                           |
| os        | string | (linux, windows)                 | *Linux*                               |
| severity  | number | 0 - 7                            | *3*                                   |
| message   | string | ---                              | *unable to update icon for discord1*  |
| timestamp | number | unix timestamp                   | *1675557738587889*                    |
| hostname  | string | ---                              | *szymon-latitude*                     |
| unit      | string | ---                              | */snap/postman/184/usr/share/postman* |
| type      | string | (application, system, logger)    | *application*                         |
| raw       | string | *                                | *raw log fetched from system*         |