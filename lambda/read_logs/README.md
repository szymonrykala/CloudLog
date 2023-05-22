# Read logs lambda function

Serverless AWS lambda function responsible for reading logs from database

## Interface
It's integrated with REST API Gateway. It handles `GET /logs` requests to the API Gateway. All data sent by the user are followed to the service because of LAMBDA PROXY integration type.

### Request
It accepts several query parameters:
* `unit` - name of the logging service or process - logging entity
* `hostname` - name of the PC/ host where the logs come from
* `type` - type of the logs [`application`|`system`|`logger`]
* `severity` - severity of the log [0-7]; default=0
* `toDate` - date in ISO 8601 format; specifies the time to which to search for logs; default=`utcnow + 10 minutes`
* `fromDate` = date in ISO 8601 format; specifies from when o search for logs. Value must be earlier than `toDate` parameter; default=`utcnow - 70 minutes`


### Response
The returned response body is in the following format:
```json
[
    {
        "os": "linux", //os type
        "severity": 3, //severity level
        "message": "message of the log",
        "timestamp": 1681642779.0976815,
        "hostname": "szymon-latitude",
        "unit": "postman_postman.desktop", //logging entity
        "raw": "kwi 16 13:11:42 szymon-latitude postman_postman.desktop[9226]: Fontconfig error: \"/etc/fonts/conf.d/80-delicious.conf\", line 6: invalid attribute 'version'", //raw log data
        "type": "application", //type of the log
        "id": "eb573694-dc48-11ed-b719-3b8ae20b0d00" // assigned id of the log
    },
    ...
]

```
If there is no results, the response array is empty.
