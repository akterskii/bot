from enum import Enum, auto
from typing import Optional, List, Tuple
from dataclasses import dataclass

from main_logic.common.patterns import MetaSingleton
from main_logic.state_handling.transitions_metadata import TransitionMetadataHandler
from transitions import Machine

class QuestStateType(Enum):
    #
    UNDEFINED_COMMAND = auto()
    # initial state
    MODE_SELECTION = auto()
    # play (start_playing)
    # edit (start_editing)

    # editor states
    EDIT_INIT = auto()
    # shows all quests
        # delete quest
        # edit quest
        # create new quest
        # level up
    EDIT_QUEST = auto()
    EDIT_CREATE_NEW = auto()
    # shows all existing steps
        # select step
        # add new
        # delete step
        # level up

    EDIT_QUEST_STEP = auto()
    # shows current step
        # edit photo
        # edit quiz
        # level up
    EDIT_QUEST_STEP_QUIZ = auto()
        #
    EDIT_QUEST_STEP_PHOTO = auto()

    # players states
    PLAY_START = auto()
    PLAY_STAGE = auto()


class Actions(Enum):
    LEVEL_UP = auto()
    EDIT_START_EDITING = auto()
    SELECT_EXISTING_QUEST = auto()
    CREATE_NEW_QUEST = auto()
    ENTER_STEP_ID = auto()
    PLAY = auto()

@dataclass
class State:
    state_type: QuestStateType
    quest_id: Optional[str] = ''
    step_id: Optional[int] = ''
    available_commands: Tuple[str] = ()


class QuestState(metaclass=MetaSingleton):
    _instance = None

    def get_state_handler(self):
        if self._instance is None:
            self._instance = QuestState()
            return self._instance

    def __init__(self):
        self.machine = Machine(
            model=self,
            states=[state.name for state in QuestStateType],
            initial=QuestStateType(1).name,
            ignore_invalid_triggers=True,
            auto_transitions=False,
        )

        # init -> editing
        self.machine.add_transition(
            trigger=Actions.EDIT_START_EDITING.name,
            source=QuestStateType.MODE_SELECTION.name,
            dest=QuestStateType.EDIT_INIT.name)
        # editing -> init
        self.machine.add_transition(
            trigger=Actions.LEVEL_UP.name,
            source=QuestStateType.EDIT_INIT.name,
            dest=QuestStateType.MODE_SELECTION.name,
        )
        # editing -> edit existing quest
        self.machine.add_transition(
            trigger=Actions.SELECT_EXISTING_QUEST.name,
            source=QuestStateType.EDIT_INIT.name,
            dest=QuestStateType.EDIT_QUEST.name,
        )
        # edit existing quest -> editing
        self.machine.add_transition(
            trigger=Actions.LEVEL_UP.name,
            source=QuestStateType.EDIT_QUEST.name,
            dest=QuestStateType.EDIT_INIT.name,
        )
        # editing -> edit new quest
        self.machine.add_transition(
            trigger=Actions.CREATE_NEW_QUEST.name,
            source=QuestStateType.EDIT_INIT.name,
            dest=QuestStateType.EDIT_QUEST.name,
        )
        self.machine.add_transition(
            trigger=Actions.ENTER_STEP_ID.name,
            source=QuestStateType.EDIT_QUEST.name,
            dest=QuestStateType.EDIT_QUEST_STEP.name,
        )
        self.machine.add_transition(
            trigger=Actions.PLAY.name,
            source=QuestStateType.MODE_SELECTION.name,
            dest=QuestStateType.PLAY_START.name,
        )
        self.machine.add_transition(
            trigger=Actions.LEVEL_UP.name,
            source=QuestStateType.PLAY_START.name,
            dest=QuestStateType.MODE_SELECTION.name,
        )
        # self.machine.add_transition(
        #     trigger=Actions..name,
        #     source=QuestStateType..name,
        #     dest=QuestStateType..name,
        # )




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
