import os
import shutil
import datetime
import hashlib
import flask
from datetime import datetime


def createTempFiles(request: flask.Request):
    tempFiles = {}
    requestHash = getHash(request)
    tempDir = f"temp/uploads/{requestHash}"
    os.makedirs(tempDir)
    for parm, file in request.files.items():
        filePath = os.path.abspath(f"{tempDir}/{file.filename}")
        file.save(filePath)
        tempFiles[parm] = filePath
    return tempFiles


def removeTempFiles(request: flask.Request):
    requestHash = getHash(request)
    tempDir = os.path.abspath(f"temp/uploads/{requestHash}")
    shutil.rmtree(tempDir)


def getHash(request: flask.Request):
    if getattr(request, 'timestamp', None) is None:
        timestamp = datetime.now().timestamp()
        if request.date is not None:
            timestamp = request.date().timestamp()
        setattr(request, "timestamp", timestamp)
    timestamp = int(request.timestamp)
    client = str(request.remote_addr)
    path = request.path
    return hashlib.sha256(f"{timestamp}_{client}_{path}".encode()).hexdigest()


flask.Request.createTempFiles = createTempFiles
flask.Request.removeTempFiles = removeTempFiles
