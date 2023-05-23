
from queue import Queue, Empty as QueueEmptyExpcetion

from . import Log


class LogQueue:
    queue = Queue()

    def push(self, *logs) -> None:
        for log in logs:
            self.queue.put(log)

    def pop(self, amount: int = 50) -> list[Log]:
        batch = []

        while len(batch) < amount:
            try:
                batch.append(self.queue.get(block=False))
            except QueueEmptyExpcetion:
                break

        return batch