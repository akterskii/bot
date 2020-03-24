from enum import Enum, auto
from typing import Optional, List, Tuple
from dataclasses import dataclass
from main_logic.state_handling.finite_state_machine import FiniteStateMachine
from main_logic.state_handling.transitions_metadata import TransitionMetadataHandler
from transitions import Machine

class QuestStateType(Enum):
    #
    UNDEFINED_COMMAND = auto()
    # initial state
    MODE_SELECTION = auto()

    # editor states
    EDIT_INIT = auto()
        # list all
        # select quest by id
        # create new
    EDIT_QUEST = auto()
        # list all steps
        # select step by id
        # add new
    EDIT_QUEST_STEP = auto()
        # edit photo
        # edit quiz
    EDIT_QUEST_STEP_QUIZ = auto()
        #
    EDIT_QUEST_STEP_PHOTO = auto()

    # players states
    PLAY_START = auto()
    PLAY_STAGE = auto()


class Actions(Enum):
    LEVEL_UP = auto()
    EDIT_QUESTS = auto()
    LIST_ALL_QUESTS = auto()


@dataclass
class State:
    state_type: QuestStateType
    quest_id: Optional[str] = ''
    step_id: Optional[int] = ''
    available_commands: Tuple[str] = ()


class QuestState:
    def __init__(self, current_state: QuestStateType):
        self.machine = Machine(
            model=self,
            states=[state.name for state in QuestStateType],
            initial=current_state.name,
        )

        self.machine.add_transition(
            trigger=Actions.EDIT_QUESTS.name,
            source=QuestStateType.MODE_SELECTION.name,
            dest=QuestStateType.EDIT_QUEST.name)

        self.machine.add_transition(
            trigger=Actions.LEVEL_UP.name,
            source=QuestStateType.EDIT_QUEST.name,
            dest=QuestStateType.MODE_SELECTION.name,
        )

# def get_fsm_for_quest():
#     quest_fsm: FiniteStateMachine[QuestStateType, TransitionMetadataHandler] = FiniteStateMachine[State, TransitionMetadataHandler]()
#
#     # adding states
#     for state in QuestStateType:
#         quest_fsm.add_state(state)
#
#     # adding transitions
#     quest_fsm.add_transition(QuestStateType.MODE_SELECTION, QuestStateType.EDIT_INIT)
#
#     quest_fsm.add_transition()
