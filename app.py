#!/usr/bin/env python3

from flask import Flask
from flask import request
from flask import make_response
from flask import Response
# import logging
# logging.basicConfig(level=logging.DEBUG)
from logging.config import dictConfig

from recorder.recorder_manager import RecorderManager, RecType
from recorder.recorder import StartRecMsg, StopRecMsg

dictConfig({
        'version': 1,
        'formatters': {
            'default': {'format': '%(asctime)s - %(levelname)s - %(message)s', 'datefmt': '%Y-%m-%d %H:%M:%S'}
        },
        'handlers': {
            'console': {
                'level': 'DEBUG',
                'class': 'logging.StreamHandler',
                'formatter': 'default',
                'stream': 'ext://sys.stdout'
            },
            'file': {
                'level': 'DEBUG',
                'class': 'logging.handlers.RotatingFileHandler',
                'formatter': 'default',
                'filename': 'debug.log',
                'maxBytes': 1024,
                'backupCount': 3
            }
        },
        'root': {
            'level': 'DEBUG',
            'handlers': ['console', 'file']
        },
        'disable_existing_loggers': False
    })

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/start', methods=['GET'])
def start_recording():

    rec_type = request.args.get('rec_type', "FFMPEG", type=str)
    file_name = request.args.get('file_name', "temp", type=str)
    rec_device = request.args.get('rec_device', 0, type=int)
    time_out = request.args.get('time_out', 600, type=int)

    app.logger.info("start req %s, %s, %s, %s", rec_type, file_name, rec_device, time_out)

    rec = RecorderManager.getRecorder(RecType[rec_type])

    exp, ack = rec.ask(StartRecMsg(file_name, rec_device, time_out))

    app.logger.info("start rsp %s, %s", exp, ack)

    if exp != None:
        return make_response(Response(str(exp)), 400)
    return make_response(Response(ack.file_name), 200)

@app.route('/stop', methods=['GET'])
def stop_recording():
    rec_type = request.args.get('rec_type', "FFMPEG", type=str)
    rec = RecorderManager.getRecorder(RecType[rec_type])
    exp, _ = rec.ask(StopRecMsg())
    if exp != None:
        return make_response(Response(str(exp)), 400)
    return make_response(Response(""), 200)
