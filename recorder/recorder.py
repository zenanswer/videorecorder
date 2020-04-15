import pykka
from enum import Enum
import logging

class _RecAct(Enum):
    Start = 1
    Stop = 2

class _RecMsg():
    def __init__(self, rec_act):
        self.recAct = rec_act

class ActState(Enum):
    Succ = 1
    Fail = 2

class StartRecMsg(_RecMsg):
    def __init__(self, file_name, rec_device=0):
        super().__init__(_RecAct.Start)
        self.file_name = file_name
        self.rec_device = rec_device

class StopRecMsg(_RecMsg):
    def __init__(self):
        super().__init__(_RecAct.Stop)

class Recorder(pykka.ThreadingActor):
    def __init__(self):
        super().__init__()

    def on_receive(self, message):
        if (not isinstance(message, _RecMsg)):
            return ActState.Fail
        action_func = { 
            _RecAct.Start: self._start,
            _RecAct.Stop: self._stop,
        }[message.recAct]
        return action_func(message)

    def _start(self, message):
        if (not isinstance(message, StartRecMsg)):
            return ActState.Fail
        logging.info("Recorder _start")
        return self.on_start_rec(message)

    def _stop(self, message):
        if (not isinstance(message, StopRecMsg)):
            return ActState.Fail
        logging.info("Recorder _stop")
        return self.on_stop_rec(message)

    def on_start_rec(self, message):
        raise Exception("Recorder not Impl on_start_rec")

    def on_stop_rec(self, message):
        raise Exception("Recorder not Impl on_stop_rec")
