import pykka
from enum import Enum
import logging

class _RecAct(Enum):
    Start = 1
    Stop = 2

class _RecMsg():
    def __init__(self, rec_act):
        self.recAct = rec_act

class StartRecMsg(_RecMsg):
    def __init__(self, file_name, rec_device=0, time_out=600):
        super().__init__(_RecAct.Start)
        self.file_name = file_name
        self.rec_device = rec_device
        self.time_out = time_out

class StartRecMsgAck(_RecMsg):
    def __init__(self, file_name):
        self.file_name = file_name

class StopRecMsg(_RecMsg):
    def __init__(self):
        super().__init__(_RecAct.Stop)

class Recorder(pykka.ThreadingActor):
    def __init__(self):
        super().__init__()
        self._running = False

    def on_receive(self, message):
        if (not isinstance(message, _RecMsg)):
            return (Exception("Not a _RecMsg message"), None)
        action_func = { 
            _RecAct.Start: self._start,
            _RecAct.Stop: self._stop,
        }[message.recAct]
        return action_func(message)

    def _start(self, message):
        if (not isinstance(message, StartRecMsg)):
            return (Exception("Not a StartRecMsg message"), None)
        logging.info("Recorder _start")
        if self._running == True:
            return (Exception("Recorder _start cannot start twice"), None)
        self._running = True
        exp, result = self.on_start_rec(message)
        if exp != None:
            self._running = False
        return (exp, result)

    def _stop(self, message):
        if (not isinstance(message, StopRecMsg)):
            return (Exception("Not a StartRecMsg message"), None)
        logging.info("Recorder _stop")
        self._running = False
        return self.on_stop_rec(message)

    def on_start_rec(self, message):
        return (Exception("Recorder not Impl on_start_rec"), StartRecMsgAck(""))

    def on_stop_rec(self, message):
        return (Exception("Recorder not Impl on_stop_rec"), None)
