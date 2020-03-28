from google.cloud import firestore
from google.cloud import storage

from main_logic.common.patterns import MetaSingleton


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