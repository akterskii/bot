import json

from google.cloud import bigquery

from main_logic.state_handling.quest_states import State


def state_file_name_by_id(user_id: int) -> str:
    fname = f'data/user_data_{user_id}.txt'
    return fname


def get_user_state(user: User) -> State:
    id = user.get_id()
    with open(file=state_file_name_by_id(user_id=id), mode='r') as inp_file:
        state = State.from_dict(json.load(inp_file))

    return state


def save_user_state(user: User, state: State):
    id = user.get_id()
    with open(file=state_file_name_by_id(user_id=id), mode="w") as out_file:
        json.dump(out_file, state)