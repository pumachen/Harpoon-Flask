import datetime
import os
import io
import sys
import json
import time
import shutil
import hou
from flask import Flask, send_file, jsonify
from xml.etree import ElementTree
from lib.serializer import *
from lib import flaskext

GAEA_CLI = "gaea.build.exe"

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
    return jsonify(HDADefinition(hda).serialize())

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


def fillHDAParm(node: hou.Node, form, files):
    for parm, value in form.items():
        values = json.loads(value)
        if not isinstance(values, str):
            values = tuple(values) if (len(values) > 1) else values[0]
        node.setParms({parm: values})
    for parm, file in files.items():
        node.parm(parm).set(file)


def hiplibrary(request):
    hips = os.listdir("HIPLibrary")
    hipLibrary = []
    for hipFile in hips:
        ext = os.path.splitext(hipFile)[1]
        if ext not in ['.hip', '.hiplc']:
            continue
        hipLibrary.append(hipFile)
    return jsonify(hipLibrary)

def hipprocessor(hip, request):
    hipPath = os.path.abspath(os.path.join("HIPLibrary", hip))
    hou.hipFile.load(hipPath, ignore_load_warnings=True)
    top = hou.node("/tasks/ENTRY")
    top.dirtyAllWorkItems(False)
    top.cookWorkItems(block=True, tops_only=False)
    return "1"

def torlibrary(request):
    tors = os.listdir("TORLibrary")
    torLibrary = []
    for torFile in tors:
        ext = os.path.splitext(torFile)[1]
        if ext not in ['.tor']:
            continue
        torLibrary.append(torFile)
    return jsonify(torLibrary)


def torprocessor(tor_name, request):
    if shutil.which(GAEA_CLI) is None:
        return r"Gaea processor not available: Gaea-CLI not found"
    tor_file = os.path.abspath(os.path.join("TORLibrary", tor_name))
    nodemap = os.path.splitext(tor_file)[0] + ".xml"
    if not os.path.exists(nodemap):
        os.system(r"{0} {1} --nodemap".format(GAEA_CLI, tor_file))
    templates = ParmTemplateGroup.FromTorNodeMap(ElementTree.parse(nodemap))
    if request.method == 'GET':
        return torprocessor_get(tor_file, templates, request)
    else:
        return torprocessor_post(tor_file, templates, request)

def torprocessor_get(tor: str, templates : ParmTemplateGroup, request):
    return jsonify(templates.serialize())

def torprocessor_post(tor, templates: ParmTemplateGroup, request):
    #os.system(r"{0} {1} --nodemap".format(GAEA_CLI, tor))
    upload_files = request.createTempFiles()
    cmd = "{0} {1} --open".format(GAEA_CLI, tor)
    variables = ""
    TEMP_DIR = os.path.abspath("./temp")
    for template in templates.parmTemplates:
        if template.isHidden:
            variables += " {0}:{1}\{2}.exr".format(template.name, TEMP_DIR, template.name)
    for parm, value in request.form.items():
        values = json.loads(value)
        if not isinstance(values, str):
            values = tuple(values) if (len(values) > 1) else values[0]
        elif len(values) == 0:
            continue
        variables += " {0}:{1}".format(parm, values)

    for parm, file in upload_files.items():
        variables += " {0}:{1}".format(parm, file)

    cmd += variables
    os.system(cmd)

    #responseFile = os.path.join(HARPOON_ROOT, r"temp/response.zip")
    #shutil.copy(topOutputFile, responseFile)

    #responseData = io.BytesIO()
    #with open(responseFile, 'rb') as fo:
    #    responseData.write(fo.read())
    #responseData.seek(0)

    #os.remove(responseFile)

    #request.removeTempFiles()

    #return send_file(responseData, mimetype="application/zip", attachment_filename="response.zip", as_attachment=True)
    return variables