import json
from dataclasses import asdict

from google.cloud import bigquery

from main_logic.common_const.common_const import USERS_STATES
from main_logic.google_cloud.clients import DatastoreClient
from main_logic.state_handling.quest_states import State
from main_logic.user_managment.users_crud import User


def get_user_state(user: User) -> State:
    user_id = user.get_id()
    state_record = DatastoreClient().get_client().collection(USERS_STATES).document(user_id)

    state = State(**state_record)

    return state


def save_user_state(user: User, state: State):
    user_id = user.get_id()
    DatastoreClient().get_client().collection(
        USERS_STATES).document(user_id).set(asdict(state))
