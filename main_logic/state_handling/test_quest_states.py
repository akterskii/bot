import pytest

from main_logic.state_handling.quest_states import QuestState, QuestStateType, Actions

def test_quest_state():
    q = QuestState(current_state=QuestStateType.MODE_SELECTION)

    print("\n\nf:", q.state)
    print("tr: ", q.machine.get_triggers(QuestStateType.MODE_SELECTION.name))
    assert False


@pytest.mark.parametrize('current_state, previous_states', [
    (QuestStateType.EDIT_QUEST, [QuestStateType.MODE_SELECTION])
])
def test_get_previous_states(current_state, previous_states):
    q = QuestState(current_state=current_state)
    print(f'cur: {q.machine.get_transitions(dest=current_state.name)}')
    print(f'all: {q.machine.get_transitions(trigger=Actions.EDIT_QUESTS.name)}')
    assert False