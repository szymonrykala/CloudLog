# Save logs lambda function

Serverless AWS lambda function responsible for saving logs in database


## Interface
Service is integrated with SQS queue.
Requests from the API Gateway `PUT /logs` are pushed to the SQS queue. Then after a while they are pushed to the lambda in a batch. It means that this is an asynchronous element of the whole system.


### SQS request
Payload of each message contains a list of logs sent by the client(logger or daemon). Format of the messages is as follows:
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
    },
    ...
]

```
Each item of the array is validated while processing the request.


### Multithreading
Lambda uses multiple threads to process a batch of messages. Each of threads accepts one message from the batch, process it and writes it to the databse.


### Resonse
The response to the SQS request contains a list of id's of failed messages - messages that processing failed due to some errors.
The response has the following schema:
```json
{
    "batchItemFailures": [
        { "itemIdentifier": "id-of-the-sqs-message" },
        { "itemIdentifier": "id-of-the-sqs-message22" },
        ...
]
}
```
This reponse is not the response that user see when callling the `PUT /logs` endpoint. 