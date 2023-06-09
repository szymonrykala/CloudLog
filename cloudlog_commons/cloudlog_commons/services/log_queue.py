from queue import Queue, Empty as QueueEmptyExpcetion

from cloudlog_commons.shared import Log


class LogQueue(Queue):
    def push(self, *logs) -> None:
        for log in logs:
            self.put(log)

    def pop(self, amount: int = 50) -> list[Log]:
        batch = []

        while len(batch) < amount:
            try:
                batch.append(self.get(block=False))
            except QueueEmptyExpcetion:
                break

        return batch
