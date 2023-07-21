import datetime
import os
import io
import sys
import json
import time
import shutil
import hou
from flask import Flask, send_file, jsonify
from lib import serializer
from lib import flaskext

def logRequestDebugInfo(request):
    # if .isInDebugMode():
    dt = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
    method = request.method
    path = request.path
    print("{} <\033[35m{}\033[0m> [\033[4;34m{}\033[0m]".format(dt, method.upper(), path))

def hdalibrary(request):
    hdas = os.listdir("HDALibrary")
    hdaLibrary = {}
    for hdaFile in hdas:
        ext = os.path.splitext(hdaFile)[1]
        if ext not in ['.hda', '.otl', '.hdalc', '.otllc']:
            continue
        hdaPath = os.path.join("HDALibrary", hdaFile)
        definition = hou.hda.definitionsInFile(hdaPath)[0]
        if not definition.isInstalled():
            hou.hda.installFile(hdaPath)
        nodeType = definition.nodeTypeCategory().name()
        if nodeType not in hdaLibrary:
            hdaLibrary[nodeType] = {}
        hdaLibrary[nodeType][hdaFile] = definition.description()
    return jsonify(hdaLibrary)

def hdaprocessor(hda_name, request):
    hdaPath = os.path.abspath(os.path.join("HDALibrary", hda_name))
    hda = hou.hda.definitionsInFile(hdaPath)[0]
    if not hda.isInstalled():
        hou.hda.installFile(hdaPath)
    else:
        hou.hda.reloadFile(hdaPath)

    if request.method == 'POST':
        return hdaprocessor_post(hda, request)
    else:
        return hdaprocessor_get(hda, request)

def hdaprocessor_get(hda, request):
    return jsonify(hda.toJson())

def hdaprocessor_post(hda, request):
    HARPOON_ROOT = os.path.abspath(".")
    hou.hipFile.save("temp/project_dump.hiplc")
    nodeTypeName = hda.nodeTypeName()
    topnet = hou.node("/tasks").createNode("topnet")
    topNode = topnet.createNode(nodeTypeName)
    uploadFiles = request.createTempFiles()
    fillHDAParm(topNode, request.form, uploadFiles)
    partition = topnet.createNode("partitionbyexpression")
    partition.setFirstInput(topNode)
    fileCompress = topnet.createNode("filecompress")
    fileCompress.setFirstInput(partition)
    topOutputFile = os.path.join(HARPOON_ROOT, r"temp/output/output.zip")
    fileCompress.parm("output_filename").set(topOutputFile)
    hou.hipFile.save("temp/project_dump.hiplc")
    fileCompress.executeGraph(filter_static=False, block=True, generate_only=False, tops_only=False)
    responseFile = os.path.join(HARPOON_ROOT, r"temp/response.zip")
    shutil.copy(topOutputFile, responseFile)
    topNode.dirtyWorkItems(True)
    topnet.destroy()

    responseData = io.BytesIO()
    with open(responseFile, 'rb') as fo:
        responseData.write(fo.read())
    responseData.seek(0)

    os.remove(responseFile)

    request.removeTempFiles()

    return send_file(responseData, mimetype="application/zip", attachment_filename="response.zip", as_attachment=True)

def hipprocessor(hip, request):
    hipPath = os.path.abspath(os.path.join("HIPLibrary", hip))
    hou.hipFile.load(hipPath, ignore_load_warnings=True)
    top = hou.node("/tasks/ENTRY")
    top.dirtyAllWorkItems(False)
    top.cookWorkItems(block=True, tops_only=False)
    return "1"

def fillHDAParm(node: hou.Node, form, files):
    for parm, value in form.items():
        values = json.loads(value)
        if not isinstance(values, str):
            values = tuple(values) if (len(values) > 1) else values[0]
        node.setParms({parm: values})
    for parm, file in files.items():
        node.parm(parm).set(file)
