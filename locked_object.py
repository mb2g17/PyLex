import threading


# An object with a lock
class LockedObject:
    # The lock
    lock = threading.Lock()

    # Constructor
    def __init__(self):
        # Sets default object value
        self.obj = None

    # Sets object value
    def set(self, obj):
        # If not locked, throw exception
        if not self.lock.locked():
            raise Exception("Tried to set LockedObject value without acquiring lock first")
        else:
            self.obj = obj

    # Gets object value
    def get(self):
        # If not locked, throw exception
        if not self.lock.locked():
            raise Exception("Tried to get LockedObject value without acquiring lock first")
        else:
            return self.obj

    # Thread-safe method to check if value is set
    def value_is_set(self):
        self.acquire_lock()
        condition = self.get() is not None
        self.release_lock()
        return condition

    # Acquires lock
    def acquire_lock(self):
        self.lock.acquire()

    # Releases lock
    def release_lock(self):
        self.lock.release()
