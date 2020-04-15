from enum import Enum

from recorder.opencv_recorder import OpenCVRecorder

class RecType(Enum):
    OpenCV = 1
    FFMPEG = 2

class RecorderManager:

    opencv_rec = OpenCVRecorder.start()
    _rec = {
        RecType.OpenCV: opencv_rec
    }

    @classmethod
    def getRecorder(cls, rec_type):
        return cls._rec[rec_type]
