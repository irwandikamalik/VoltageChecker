from app.core.state import (
    ProcessState,
    StateManager
)


state_manager = StateManager()


def show_state():

    print(
        "Current state:",
        state_manager.get_state()
    )


print("=== NORMAL TEST FLOW ===")


show_state()


state_manager.set_state(
    ProcessState.OPERATOR_VALID
)

show_state()


state_manager.set_state(
    ProcessState.BATCH_READY
)

show_state()


state_manager.set_state(
    ProcessState.WAIT_SERIAL
)

show_state()


state_manager.set_state(
    ProcessState.SERIAL_VALID
)

show_state()


state_manager.set_state(
    ProcessState.TESTING
)

show_state()


state_manager.set_state(
    ProcessState.RESULT_NG
)

show_state()


state_manager.set_state(
    ProcessState.RETEST
)

show_state()


state_manager.set_state(
    ProcessState.TESTING
)

show_state()


state_manager.set_state(
    ProcessState.RESULT_OK
)

show_state()


state_manager.set_state(
    ProcessState.COMPLETED
)

show_state()


state_manager.set_state(
    ProcessState.WAIT_SERIAL
)

show_state()