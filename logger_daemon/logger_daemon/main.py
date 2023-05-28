import os
import sys
import threading
import time
import subprocess
import platform
import json
from cloudlog_commons import Log, OS, LogType, LogQueue, LogSender

class LogWorker(threading.Thread):
    
    def __init__(self, num_logs, interval):
        super().__init__()
        self.num_logs = num_logs
        self.interval = interval
        self.stopped = False
        self.batch = []

    def stop(self):
        self.stopped = True
        LogSender.stop()
        LogSender.join()

    def get_logs(self):
        if platform.system() == 'Windows':
            logs = self.get_windows_logs()
        else:
            logs = self.get_linux_logs()
        return logs

    def get_windows_logs(self): #Get-WinEvent -FilterHashtable @{Logname="Application","System"; StartTime=(Get-Date).AddSeconds(-60)} -MaxEvents 100 | Select-Object @{Name="TimeCreated";Expression={$_.TimeCreated.ToUniversalTime().Subtract((Get-Date "1/1/1970")).TotalSeconds}}, Level, Message, ProviderName, MachineName, ContainerLog | ConvertTo-Json
        cmd = f"powershell -Command Get-WinEvent -FilterHashtable @{{logname=\'Application\',\'System\'; StartTime=(Get-Date).AddSeconds(-{self.interval})}} -MaxEvents {self.num_logs} | Select-Object @{{Name=\'TimeCreated\';Expression={{$_.TimeCreated.ToUniversalTime().Subtract((Get-Date \'1/1/1970\')).TotalSeconds}}}}, Level, Message, ProviderName, MachineName, ContainerLog | ConvertTo-Json"
        result = []
        try:
            output = subprocess.check_output(cmd, encoding='utf-8', errors='replace')
            logs = json.loads(output)
            #print(f"logs fetched: {len(logs)}")
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
            return result
        except:
            print(f"no logs / error")
            return None
    
    def get_linux_logs(self):   #cmd = f'journalctl --lines=100 --since="-10s" --output=json | jq \'.[] | {{os: "Linux", severity: .PRIORITY, message: .MESSAGE, timestamp: (.__REALTIME_TIMESTAMP / 1000000 | floor | str | tonumber), hostname: ._HOSTNAME, unit: ._EXE}}\''
        cmd = f'journalctl --lines={self.num_logs} --since="-{self.interval}s" --output=json | jq \'.[] | {{os: "Linux", severity: .PRIORITY, message: .MESSAGE, timestamp: (.__REALTIME_TIMESTAMP / 1000000 | floor | str | tonumber), hostname: ._HOSTNAME, unit: ._EXE}}\''
        result = []
        try:
            output = subprocess.check_output(cmd, encoding='utf-8', errors='replace', executable="/bin/bash")
            logs = json.loads(output)
            #print(f"logs fetched: {len(logs)}")
            for log in logs:
                result.append(Log(
                    OS.LINUX.value,
                    log['severity'],
                    log['message'],
                    log['timestamp'],
                    log['hostname'],
                    log['unit'],
                    log,
                    LogType.APP.value if "snap" in log['unit'] or "opt" in log['unit'] else LogType.LOGGER.value))
            return result
        except:
            print("no logs / error")
            return None

    def run(self):
        while not self.stopped:    
            logs = self.get_logs()
            if logs is not None:
                queue = LogQueue.push(logs)
                LogSender.attach_queue(queue)
            LogSender.start()
            time.sleep(self.interval)

def run_log_service():
    interval = int(os.environ.get('interval', 10)) #time in sec since when a single powershell/bash command gets the logs
    num_logs = int(os.environ.get('NUM_LOGS', 100)) #max number of logs from single pwsh/bash call  

    log_worker = LogWorker(num_logs, interval)
    
    try:
        log_worker.start()
        input("Press enter to stop...")
    except KeyboardInterrupt:
        print("Stopping...")
    finally:
        log_worker.stop()
        log_worker.join()

if __name__ == '__main__':
    if sys.argv[0] == 'background':
        # Run the log service in the background Linux only
        pid = os.fork()
        if pid > 0:
            # Parent process, exit
            sys.exit()
        elif pid == 0:
            # Child process, continue running
            run_log_service()
    else:
        # Run the log service in the foreground
        run_log_service()
