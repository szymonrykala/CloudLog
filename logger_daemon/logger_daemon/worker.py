import json
import platform
import subprocess
import threading
import time

from logs import LinuxLog, WindowsLog

from cloudlog_commons.services import LogQueue


class LogWorker(threading.Thread):
    _logger = None
    __logs_queue = None

    def __init__(self, interval, logger=_logger):
        super().__init__()
        
        self._logger = logger
        self.interval: int = interval
        self.stopped: bool = False

        self.__LOG_CLASS, self.__CMD = self.__get_system_specific_config()
        self._logger.info(f"Determined system specific config: {self.__LOG_CLASS}, {self.__CMD}")
        

    @classmethod
    def attach_queue(cls, queue: LogQueue):
        cls.__logs_queue = queue

    @property
    def linux_cmd(self):
        return [
            "bash",
            "-c",
            f"journalctl --since=-{self.interval}s --output=json | jq -c -s .",
        ]

    @property
    def windows_cmd(self):
        return [
            "powershell",
            "-Command",
            f"Get-WinEvent -FilterHashtable @{{logname='Application','System'; StartTime=(Get-Date).AddSeconds(-{self.interval})}} | ConvertTo-Json",
        ]

    def __get_system_specific_config(self):
        if platform.system() == "Windows":
            return WindowsLog, self.windows_cmd

        return LinuxLog, self.linux_cmd

    def stop(self):
        self._logger.info(f"Shutting down {self}")
        self.stopped = True

    def __get_logs(self):
        try:
            process = subprocess.Popen(
                self.__CMD,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                encoding="utf8"
            )
            output, error = process.communicate()           
            if error:
                raise Exception(f"Command error: {error}")

            self._logger.info(output)

            for log in json.loads(output or "[]"):
                try:
                    yield self.__LOG_CLASS.from_dict(log)
                except Exception as exc:
                    self._logger.warning(f"Log record processing failed with error: {exc}")

        except Exception as err:
            self._logger.warning("Getting logs failed")
            self._logger.error(f"Command {self.__CMD} failed with error: '{err}'")

    def run(self):
        self._logger.info("Daemon is running ...")
        while not self.stopped:
            logs = tuple(self.__get_logs())
            if logs:
                self.__logs_queue.push(logs)

            time.sleep(self.interval)
