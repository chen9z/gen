from threading import Semaphore, Lock
from typing import Any, Optional


class State:

    def __init__(self, value: Optional[Any] = None):
        self._value = value
        self.semaphore = Semaphore(0)
        self._lock = Lock()

    def get_value(self) -> Optional[Any]:
        self.semaphore.acquire()
        output = self._value
        self.semaphore.release()
        return output

    def get_value_with_lock(self) -> Optional[Any]:
        with self._lock:
            return self._value

    def set_value(self, value: Optional[Any]):
        with self._lock:
            self._value = value
        self.semaphore.release()

    @classmethod
    def empty(cls):
        return cls(None)
