import dataclasses
from dataclasses import asdict
from typing import Optional, Dict, Any, List

from google.cloud import firestore
from dataclasses import dataclass

from main_logic.common_const.common_const import USERS_COLLECTION


class MetaSingleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(MetaSingleton, cls).__call__(*args,
                                                                     **kwargs)
        return cls._instances[cls]


class DatastoreClient(metaclass=MetaSingleton):
    _datastore_client = None

    def get_client(self):
        if self._datastore_client is None:
            self._datastore_client = firestore.Client()
        return self._datastore_client


class UserNotFound(Exception):
    """Custom exception for the user not found case"""


class ManyUsersWithSameID(Exception):
    """Custom exception for the many users with same id"""


def dicts_to_dataclasses(instance):
    """Convert all fields of type `dataclass` into an instance of the
    specified data class if the current value is of type dict."""
    cls = type(instance)
    for f in dataclasses.fields(cls):
        if not dataclasses.is_dataclass(f.type):
            continue

        value = getattr(instance, f.name)
        if not isinstance(value, dict):
            continue

        new_value = f.type(**value)
        setattr(instance, f.name, new_value)


@dataclass
class WebCredentials:
    def __post_init__(self):
        dicts_to_dataclasses(instance=self)

    user_name: str
    password_hash: str
    registration_date: str
    email: Optional[str]


@dataclass
class User:
    def __post_init__(self):
        dicts_to_dataclasses(instance=self)

    user_id: str
    first_name: Optional[str] = ''
    last_name: Optional[str] = ''
    telegram_id: Optional[str] = ''
    web_credentials: Optional[WebCredentials] = None

    @staticmethod
    def get_user_by_telegram_id(telegram_id: str) -> Optional['User']:
        client = DatastoreClient().get_client()
        users = client.collection(USERS_COLLECTION).where(
            u'telegram_id', u'==', telegram_id).stream()

        users = list(users)

        if len(users) == 0:
            raise UserNotFound
        elif len(users) > 1:
            raise ManyUsersWithSameID
        return User(**(users[0].to_dict()))

    def update_db(self):
        try:
            users = DatastoreClient().get_client().collection(USERS_COLLECTION)
            users.document(self.user_id).update(asdict(self))
            return True
        except Exception as e:
            print(e)
            return False

    def add_to_db(self):
        try:
            new_user = DatastoreClient().get_client().collection(USERS_COLLECTION).document()
            self.user_id = new_user.id
            new_user.set(asdict(self))
            return new_user.id
        except Exception as e:
            print(e)
            return None


@dataclass
class State:
    pass


@dataclass
class Quest:
    pass


@dataclass
class StepWithImages:
    def __post_init__(self):
        dicts_to_dataclasses(instance=self)

    image_id: str
    images_in_gcloud: List[str]
    images_in_telegram: List[str]