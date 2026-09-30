from enum import Enum


class TestState(Enum):

    IDLE = "IDLE"

    OPERATOR_VALID = "OPERATOR_VALID"

    BATCH_READY = "BATCH_READY"

    WAIT_SERIAL = "WAIT_SERIAL"

    SERIAL_VALID = "SERIAL_VALID"

    TESTING = "TESTING"

    RESULT_OK = "RESULT_OK"

    RESULT_NG = "RESULT_NG"

    RETEST = "RETEST"

    COMPLETED = "COMPLETED"

    ERROR = "ERROR"


class TestStateManager:

    def __init__(self):

        self.current_state = TestState.IDLE

        self.transitions = {

            TestState.IDLE: [
                TestState.OPERATOR_VALID
            ],

            TestState.OPERATOR_VALID: [
                TestState.BATCH_READY,
                TestState.ERROR
            ],

            TestState.BATCH_READY: [
                TestState.WAIT_SERIAL,
                TestState.ERROR
            ],

            TestState.WAIT_SERIAL: [
                TestState.SERIAL_VALID,
                TestState.ERROR
            ],

            TestState.SERIAL_VALID: [
                TestState.TESTING,
                TestState.ERROR
            ],

            TestState.TESTING: [
                TestState.RESULT_OK,
                TestState.RESULT_NG,
                TestState.ERROR
            ],

            TestState.RESULT_OK: [
                TestState.COMPLETED
            ],

            TestState.RESULT_NG: [
                TestState.RETEST,
                TestState.COMPLETED
            ],

            TestState.RETEST: [
                TestState.TESTING,
                TestState.ERROR
            ],

            TestState.COMPLETED: [
                TestState.WAIT_SERIAL
            ],

            TestState.ERROR: [
                TestState.IDLE
            ]
        }
        

    def get_state(self):

        return self.current_state


    def can_transition(self, new_state):

        allowed_states = self.transitions.get(
            self.current_state,
            []
        )

        return new_state in allowed_states


    def set_state(self, new_state):

        if not self.can_transition(new_state):

            raise ValueError(
                "Tidak dapat berpindah dari {} ke {}".format(
                    self.current_state.value,
                    new_state.value
                )
            )

        self.current_state = new_state