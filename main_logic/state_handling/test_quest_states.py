from main_logic.state_handling.quest_states import QuestState, QuestStateType


def test_quest_state():
    q = QuestState(current_state=QuestStateType.MODE_SELECTION)
    print(q.machine.get_transitions())