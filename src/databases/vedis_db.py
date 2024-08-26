from vedis import Vedis
from threading import Lock
lock = Lock()


class VedisClient:
    """
    Класс для работы конечного автомата
    """
    def __init__(self):
        self.db = Vedis('db.vdb')
        self.uniq_value = 'uniq_value'
        self.key_command = 'command'
        self.key_task_name = 'task_name'
        self.status = 'status'

    async def get_object(self, key):
        with lock:
            try:
                return self.db[key].decode()
            except KeyError:
                return None

    async def set_object(self, object_, key):
        with lock:
            self.db[key] = object_
            self.db.commit()

    def __getitem__(self, item):
        return self.db[item]


db_client = VedisClient()


