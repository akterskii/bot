import pytest

from main_logic.common.common_const import USERS_STATES
from main_logic.google_cloud.clients import DatastoreClient
from main_logic.state_handling.quest_states import State, QuestStateType
from main_logic.state_handling.state_handler import get_possible_transitions


def test_get_user_state():
    user_id = "SQlsjGgfH4Oq3WhC7BHA"
    collect_ref = DatastoreClient().get_client().collection(USERS_STATES)
    collect_ref2 = DatastoreClient().get_client().collection(USERS_STATES+'fasd')
    print(f'ref: {collect_ref} ref2: {collect_ref2}')
    collect_ref.document(u'fdsfafsa').set({"state":"fds"})
    doc_ref = collect_ref.document(user_id)
    print(f'ref: {doc_ref}')
    state_record = doc_ref.get().to_dict()
    print(f'user_id: {user_id}, state_record: {state_record}')
    state = None
    if state_record:
        state = State(**state_record)
    print(f'parsed_state: {state}')
    assert False

@pytest.mark.parametrize('cur_state',[
    QuestStateType.MODE_SELECTION,
    QuestStateType.EDIT_INIT,
])
def test_get_possible_transitions(cur_state: QuestStateType):
    actions, action_strings = get_possible_transitions(cur_state=cur_state)
    print(actions, action_strings)
    assert False