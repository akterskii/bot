import json
from dataclasses import asdict
from typing import Optional

from google.cloud import bigquery

from main_logic.common.common_const import USERS_STATES, INITIAL_STATE
from main_logic.common.mappings import ACTIONS_TO_COMMAND
from main_logic.google_cloud.clients import DatastoreClient
from main_logic.state_handling.quest_states import State, QuestStateType, QuestState, Actions
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


def init_user_state(user_id: str) -> bool:
    state_ref = DatastoreClient().get_client().collection(
        USERS_STATES).document(user_id)
    state_ref.set({u'state_type': INITIAL_STATE.name})


def update_user_state(user: User, new_state: QuestStateType) -> bool:
    try:
        user_id = user.get_id()
        state_ref = DatastoreClient().get_client().collection(USERS_STATES).document(user_id)
        state_ref.update({u'state_type': new_state.name})
        return True
    except Exception as e:
        print(f'Update of state failed for user {user} to state: {new_state}. '
              f'Exception: {e}')
        return False


def get_possible_commands(cur_state: QuestStateType):
    print(f'cur_state: {cur_state}. type {type(cur_state)}')
    q = QuestState()
    actions = q.machine.get_triggers(cur_state.name)
    actions_strings = set(map(lambda x: ACTIONS_TO_COMMAND.get(Actions[x]), actions))
    return actions_strings


def save_user_state(user: User, state: State):
    user_id = user.get_id()
    DatastoreClient().get_client().collection(
        USERS_STATES).document(user_id).set(asdict(state))
