from enum import Enum


class ProcessState(Enum):

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


class StateManager:

    def __init__(self):

        self.current_state = ProcessState.IDLE

        self.transitions = {

            ProcessState.IDLE: [
                ProcessState.OPERATOR_VALID,
                ProcessState.ERROR
            ],

            ProcessState.OPERATOR_VALID: [
                ProcessState.BATCH_READY,
                ProcessState.ERROR
            ],

            ProcessState.BATCH_READY: [
                ProcessState.WAIT_SERIAL,
                ProcessState.ERROR
            ],

            ProcessState.WAIT_SERIAL: [
                ProcessState.SERIAL_VALID,
                ProcessState.ERROR
            ],

            ProcessState.SERIAL_VALID: [
                ProcessState.TESTING,
                ProcessState.ERROR
            ],

            ProcessState.TESTING: [
                ProcessState.RESULT_OK,
                ProcessState.RESULT_NG,
                ProcessState.ERROR
            ],

            ProcessState.RESULT_OK: [
                ProcessState.COMPLETED
            ],

            ProcessState.RESULT_NG: [
                ProcessState.RETEST,
                ProcessState.COMPLETED
            ],

            ProcessState.RETEST: [
                ProcessState.TESTING,
                ProcessState.ERROR
            ],

            ProcessState.COMPLETED: [
                ProcessState.WAIT_SERIAL
            ],

            ProcessState.ERROR: [
                ProcessState.IDLE
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