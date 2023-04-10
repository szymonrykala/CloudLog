import os
import threading
import queue
import time
import subprocess
import requests
import platform
import json
from cloudlog_commons import Log, OS, LogType


class LogWorker(threading.Thread):
    def __init__(self, num_logs, batch_size, time_in_minutes):
        super().__init__()
        self.num_logs = num_logs
        self.batch_size = batch_size
        self.time_in_minutes = time_in_minutes
        self.stopped = False

    def stop(self):
        self.stopped = True

    def get_logs(self):
        if platform.system() == 'Windows':
            logs = self.get_windows_logs()
        else:
            logs = self.get_linux_logs()
        return logs

    def get_windows_logs(self): #Get-WinEvent -FilterHashtable @{Logname="Application","System"; StartTime=(Get-Date).AddMinutes(-60)} -MaxEvents 100 | Select-Object @{Name="TimeCreated";Expression={$_.TimeCreated.ToUniversalTime().Subtract((Get-Date "1/1/1970")).TotalSeconds}}, Level, Message, ProviderName, MachineName, ContainerLog | ConvertTo-Json
        cmd = f"powershell -Command Get-WinEvent -FilterHashtable @{{logname=\'Application\',\'System\'; StartTime=(Get-Date).AddMinutes(-{self.time_in_minutes})}} -MaxEvents {self.num_logs} | Select-Object @{{Name=\'TimeCreated\';Expression={{$_.TimeCreated.ToUniversalTime().Subtract((Get-Date \'1/1/1970\')).TotalSeconds}}}}, Level, Message, ProviderName, MachineName, ContainerLog | ConvertTo-Json"
        result = []
        try:
            output = subprocess.check_output(cmd, encoding='utf-8', errors='replace')
            logs = json.loads(output)
            print(f"logs fetched: {len(logs)}")
            for log in logs:
                result.append(Log(
                    OS.WINDOWS.value,
                    log['Level'],
                    log['Message'],
                    log['TimeCreated'],
                    log['MachineName'],
                    log['ProviderName'],
                    log, 
                    LogType.SYSTEM.value if (log['ContainerLog'] == "System") else LogType.APP.value if (log['ContainerLog'] == "Application") else LogType.LOGGER.value))
            print(result)
            return result
        except subprocess.CalledProcessError as e:
            print(f"PWSH Error / no logs")
            return None
    
    def get_linux_logs(self):   #cmd = f'journalctl --lines=100 --since="60 min ago" --output=json | jq \'.[] | {{os: "Linux", severity: .PRIORITY, message: .MESSAGE, timestamp: (.__REALTIME_TIMESTAMP / 1000000 | floor | str | tonumber), hostname: ._HOSTNAME, unit: ._EXE}}\''
        cmd = f'journalctl --lines={self.num_logs} --since="{self.time_in_minutes} min ago" --output=json | jq \'.[] | {{os: "Linux", severity: .PRIORITY, message: .MESSAGE, timestamp: (.__REALTIME_TIMESTAMP / 1000000 | floor | str | tonumber), hostname: ._HOSTNAME, unit: ._EXE}}\''
        result = ""
        try:
            output = subprocess.check_output(cmd, encoding='utf-8', errors='replace', executable="/bin/bash")
            logs = json.loads(output)
            print(f"logs fetched: {len(logs)}")
            for log in logs:
                result.append(Log(
                    OS.LINUX.value,
                    log['severity'],
                    log['message'],
                    log['timestamp'],
                    log['hostname'],
                    log['unit'],
                    log,
                    LogType.APP.value if "snap" in log['unit'] or "opt" in log['unit'] else LogType.SYSTEM.value))
            print(result)
            return result
        except:
            print("no logs")
            return None

    def run(self):
        batch = []
        while not self.stopped:    
            logs = self.get_logs()
            if logs is not None:
                for log in logs:
                    batch.append(log)
            if len(batch) >= self.batch_size:
                log_queue.put(batch)
                batch = []
            time.sleep(self.time_in_minutes*60)

class LogSender(threading.Thread):
    def __init__(self, endpoint):
        super().__init__()
        self.endpoint = endpoint
        self.stopped = False

    def stop(self):
        self.stopped = True

    def run(self):
        while not self.stopped or not log_queue.empty():
            try:
                batch = log_queue.get(timeout=1)
            except queue.Empty:
                continue
            try:
                response = requests.post(self.endpoint, json=batch)
                if response.status_code == 200:
                    num_logs = sum([len(item) for item in batch])
                    print(f"Sent batch with {num_logs} logs")
                else:
                    print(f"Failed to send logs with status code {response.status_code}")
            except requests.exceptions.RequestException as e:
                print(f"Failed to send logs: {e}")
            time.sleep(10)

if __name__ == '__main__':
    time_in_minutes = int(os.environ.get('TIME_IN_MINUTES', 1)) #time in minutes since when a single powershell/bash command gets the logs
    num_logs = int(os.environ.get('NUM_LOGS', 100)) #max number of logs from single pwsh/bash call  
    batch_size = int(os.environ.get('BATCH_SIZE', 10))  #how many logs do you want to send in one request
    endpoint = "http://localhost:5000/logs"

    log_queue = queue.Queue()
    log_worker = LogWorker(num_logs, batch_size, time_in_minutes)
    log_sender = LogSender(endpoint)

    try:
        log_worker.start()
        log_sender.start()
        input("Press enter to stop...")
    except KeyboardInterrupt:
        print("Stopping...")
    finally:
        log_worker.stop()
        log_worker.join()
        log_sender.stop()
        log_sender.join()
