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
    rec_type = request.args.get('rec_type')
    file_name = request.args.get('file_name')
    rec = RecorderManager.getRecorder(RecType[rec_type])
    result, file_name = rec.ask(StartRecMsg(file_name))
    return make_response(Response(result.name+':'+file_name), 200)

@app.route('/stop', methods=['GET'])
def stop_recording():
    rec_type = request.args.get('rec_type')
    rec = RecorderManager.getRecorder(RecType[rec_type])
    result = rec.ask(StopRecMsg())
    return make_response(Response(result.name), 200)
