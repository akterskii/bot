from main_logic.state_handling.quest_states import Actions

ACTIONS_TO_COMMAND = {
    Actions.EDIT_START_EDITING: 'edit',
    Actions.LEVEL_UP: 'back',
    Actions.CREATE_NEW_QUEST: 'new',
    Actions.SELECT_EXISTING_QUEST: 'quest_id',
    Actions.ENTER_STEP_ID: 'step_id',
    Actions.PLAY: 'play'
}

COMMANDS_TO_ACTIONS = {
    command: action for action, command in ACTIONS_TO_COMMAND.items()}
