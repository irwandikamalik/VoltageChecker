from app.core.test_state import (
    TestState,
    TestStateManager
)


state_manager = TestStateManager()


def show_state():

    print(
        "Current state:",
        state_manager.get_state()
    )


print("=== NORMAL TEST FLOW ===")


show_state()


state_manager.set_state(
    TestState.OPERATOR_VALID
)

show_state()


state_manager.set_state(
    TestState.BATCH_READY
)

show_state()


state_manager.set_state(
    TestState.WAIT_SERIAL
)

show_state()


state_manager.set_state(
    TestState.SERIAL_VALID
)

show_state()


state_manager.set_state(
    TestState.TESTING
)

show_state()


state_manager.set_state(
    TestState.RESULT_NG
)

show_state()


state_manager.set_state(
    TestState.RETEST
)

show_state()


state_manager.set_state(
    TestState.TESTING
)

show_state()


state_manager.set_state(
    TestState.RESULT_OK
)

show_state()


state_manager.set_state(
    TestState.COMPLETED
)

show_state()


state_manager.set_state(
    TestState.WAIT_SERIAL
)

show_state()