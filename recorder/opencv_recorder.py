from recorder.recorder import Recorder, ActState
import logging
from datetime import datetime
import cv2
import time
import threading

class RecordingThread(threading.Thread):
    def __init__(self, file_name):
        threading.Thread.__init__(self)
        self._running = False
        self._file_name = file_name

    def run(self):
        self._running = True

        cap = cv2.VideoCapture(0)

        frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

        out = cv2.VideoWriter(self._file_name,
                cv2.VideoWriter_fourcc(*'mp4v'), 
                30,
                (frame_width, frame_height))
        interval = 1.00/30

        while cap.isOpened() and self._running:
            # logging.info("video_recording")
            ret, frame = cap.read()
            time_string = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
            if ret:
                cv2.putText(frame, time_string, 
                    (10, 50), 
                    cv2.FONT_HERSHEY_SIMPLEX, 
                    1,
                    (255, 255, 255),
                    1)
                out.write(frame)
            time.sleep(interval)

        out.release()
        cap.release()

    def stop(self):
        self._running = False

    def getFileName(self):
        return self._file_name


class OpenCVRecorder(Recorder):
    def __init__(self):
        super().__init__()
        self._thread = None

    def on_start_rec(self, message):
        logging.info("OpenCVRecorder on_start_rec")
        if self._thread is not None:
            return ActState.Fail

        file_name = message.file_name
        time_string = datetime.now().strftime("%Y%m%d-%H%M%S_")
        self._file_name = time_string+file_name+'.mp4'

        self._thread = RecordingThread(self._file_name)
        self._thread.start()
        return (ActState.Succ, self._file_name)

    def on_stop_rec(self, message):
        logging.info("OpenCVRecorder on_stop_rec")
        self._thread.stop()
        self._thread.join()
        self._thread = None
        return ActState.Succ
