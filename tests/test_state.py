from app.core.state import ProcessState, StateManager


def test_initial_state():

    state_manager = StateManager()

    assert state_manager.get_state() == ProcessState.IDLE


def test_valid_transition():

    state_manager = StateManager()

    state_manager.set_state(
        ProcessState.OPERATOR_VALID
    )

    assert (
        state_manager.get_state()
        == ProcessState.OPERATOR_VALID
    )


def test_invalid_transition():

    state_manager = StateManager()

    try:
        state_manager.set_state(
            ProcessState.TESTING
        )
        assert False
    except ValueError:
        assert True


def test_testing_to_result_ok():

    state_manager = StateManager()

    state_manager.set_state(
        ProcessState.OPERATOR_VALID
    )
    state_manager.set_state(
        ProcessState.BATCH_READY
    )
    state_manager.set_state(
        ProcessState.WAIT_SERIAL
    )
    state_manager.set_state(
        ProcessState.SERIAL_VALID
    )
    state_manager.set_state(
        ProcessState.TESTING
    )
    state_manager.set_state(
        ProcessState.RESULT_OK
    )

    assert (
        state_manager.get_state()
        == ProcessState.RESULT_OK
    )


def test_testing_to_result_ng():

    state_manager = StateManager()

    state_manager.set_state(
        ProcessState.OPERATOR_VALID
    )
    state_manager.set_state(
        ProcessState.BATCH_READY
    )
    state_manager.set_state(
        ProcessState.WAIT_SERIAL
    )
    state_manager.set_state(
        ProcessState.SERIAL_VALID
    )
    state_manager.set_state(
        ProcessState.TESTING
    )
    state_manager.set_state(
        ProcessState.RESULT_NG
    )

    assert (
        state_manager.get_state()
        == ProcessState.RESULT_NG
    )


def test_retest_flow():

    state_manager = StateManager()

    state_manager.set_state(
        ProcessState.OPERATOR_VALID
    )
    state_manager.set_state(
        ProcessState.BATCH_READY
    )
    state_manager.set_state(
        ProcessState.WAIT_SERIAL
    )
    state_manager.set_state(
        ProcessState.SERIAL_VALID
    )
    state_manager.set_state(
        ProcessState.TESTING
    )
    state_manager.set_state(
        ProcessState.RESULT_NG
    )
    state_manager.set_state(
        ProcessState.RETEST
    )
    state_manager.set_state(
        ProcessState.TESTING
    )

    assert (
        state_manager.get_state()
        == ProcessState.TESTING
    )