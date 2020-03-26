import json
from dataclasses import asdict
from typing import Optional

from google.cloud import bigquery

from main_logic.common.common_const import USERS_STATES
from main_logic.google_cloud.clients import DatastoreClient
from main_logic.state_handling.quest_states import State, QuestStateType
from main_logic.user_managment.users_crud import User


def get_user_state(user: User) -> Optional[State]:
    user_id = user.get_id()
    state_record = DatastoreClient().get_client().collection(USERS_STATES).document(user_id).get().to_dict()
    print(f'user_id: {user_id}, state_record: {state_record}')
    state = None
    if state_record:
        state = State(**state_record)
    print(f'parsed_state: {state}')
    return state


def update_user_state(user: User, new_state: QuestStateType) -> bool:
    try:
        user_id = user.get_id()
        state_ref = DatastoreClient().get_client().collection(USERS_STATES).document(user_id)
        state_ref.update({u'state': new_state.name})
        return True
    except Exception as e:
        print(f'Update of state failed for user {user} to state: {new_state}. '
              f'Exception: {e}')
        return False

def save_user_state(user: User, state: State):
    user_id = user.get_id()
    DatastoreClient().get_client().collection(
        USERS_STATES).document(user_id).set(asdict(state))
