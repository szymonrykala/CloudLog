from dataclasses import dataclass


@dataclass
class CloudLogBaseException(Exception):
    statusCode: int = 500
    message: str = "InternalServerError"
    

class LogEntryValidationError(CloudLogBaseException):
    statusCode:int = 400
    
    def __init__(self, message:str = "Request data are not valid"):
        self.message = message


class DynamoRequestException(CloudLogBaseException):
    statusCode:int = 400

    def __init__(self, message):
        self.message = f"Failed to execute dynamo request: {message}"
    