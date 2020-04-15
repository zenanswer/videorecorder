from recorder.recorder import Recorder, StartRecMsgAck
import logging
from datetime import datetime
import subprocess
import time
import threading


class RecordingThread(threading.Thread):
    def __init__(self, file_name, time_out):
        threading.Thread.__init__(self)
        self._file_name = file_name
        self._time_out = time_out
        self._proc = None

    def run(self):
        cmd = "ffmpeg -f v4l2 " \
            "-framerate 30 -video_size hd720 -c:v h264 -i /dev/video%d " \
            "-c:v copy %s" % (2, self._file_name)
        print(cmd)
        self._proc = subprocess.Popen(cmd.split(" "), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        try:
            outs, errs = self._proc.communicate(timeout=self._time_out)
            print(outs, errs)
        except subprocess.TimeoutExpired:
            self._proc.terminate()
            outs, errs = self._proc.communicate()
        except Exception as exp:
            print(exp)

    def stop(self):
        self._proc.terminate()
        outs, errs = self._proc.communicate()
        print(outs, errs)

    def getFileName(self):
        return self._file_name

class FFmpegRecorder(Recorder):
    def __init__(self):
        super().__init__()
        self._thread = None

    def on_start_rec(self, message):
        logging.info("FFmpegRecorder on_start_rec")
        if self._thread is not None:
            return (Exception("FFmpegRecorder on_start_rec cannot start twice"), None)

        file_name = message.file_name
        time_string = datetime.now().strftime("%Y%m%d-%H%M%S_")
        self._file_name = time_string+file_name+'.mp4'

        self._thread = RecordingThread(self._file_name, message.time_out)
        self._thread.start()

        return (None, StartRecMsgAck(self._file_name))

    def on_stop_rec(self, message):
        logging.info("FFmpegRecorder on_stop_rec")
        if self._thread is not None:
            self._thread.stop()
            self._thread.join()
            self._thread = None
        return (None, None)
