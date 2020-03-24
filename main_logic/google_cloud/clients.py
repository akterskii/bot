from google.cloud import firestore
from google.cloud import storage


class MetaSingleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(MetaSingleton, cls).__call__(*args,
                                                                     **kwargs)
        return cls._instances[cls]


class DatastoreClient(metaclass=MetaSingleton):
    _datastore_client = None

    def get_client(self) -> firestore.Client:
        if self._datastore_client is None:
            self._datastore_client = firestore.Client()
        return self._datastore_client


class StorageClient(metaclass=MetaSingleton):
    _storage_client = None

    def get_client(self) -> storage.Client:
        if self._storage_client is None:
            self._storage_client = storage.Client()
        return self._storage_client