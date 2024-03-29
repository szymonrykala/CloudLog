from cloudlog_commons.cloud.exceptions import CloudLogBaseException


class BadRequestParameterValue(CloudLogBaseException):
    statusCode:int = 400
    
    def __init__(self, message:str):
        self.message = message