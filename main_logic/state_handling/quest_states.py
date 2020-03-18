from enum import Enum, auto
from typing import Optional
from dataclasses import dataclass
from main_logic.state_handling.finite_state_machine import FiniteStateMachine
from main_logic.state_handling.transitions_metadata import TransitionMetadataHandler


class QuestStateType(Enum):
    #
    UNDEFINED_COMMAND = auto
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


@dataclass(frozen=True)
class State:
    state_type: QuestStateType
    quest_id: Optional[int]
    step_id: Optional[int]


def get_fsm_for_quest():
    quest_fsm: FiniteStateMachine[QuestStateType, TransitionMetadataHandler] = FiniteStateMachine[State, TransitionMetadataHandler]()

    # adding states
    for state in QuestStateType:
        quest_fsm.add_state(state)

    # adding transitions
    quest_fsm.add_transition(QuestStateType.MODE_SELECTION, QuestStateType.EDIT_INIT)

    quest_fsm.add_transition()
