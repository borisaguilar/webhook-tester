import threading

class Database:
    def __init__(self):
        self.value = []
        self._lock = threading.Lock()

    def push(self, item):
        with self._lock:
            self.value += [item]
    def pop_all(self):
        with self._lock:
            __tmp = self.value
            self.value = []
            return __tmp
