from enum import Enum

from recorder.opencv_recorder import OpenCVRecorder
from recorder.ffmpeg_recorder import FFmpegRecorder

class RecType(Enum):
    OpenCV = 1
    FFMPEG = 2

class RecorderManager:

    opencv_rec = OpenCVRecorder.start()
    ffmpeg_rec = FFmpegRecorder.start()
    _rec = {
        RecType.OpenCV: opencv_rec,
        RecType.FFMPEG: ffmpeg_rec,
    }


    @classmethod
    def getRecorder(cls, rec_type):
        return cls._rec[rec_type]
