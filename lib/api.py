import os
import hou
import sys
import json
import time
import shutil
import hwebserver


def logRequestDebugInfo(request: hwebserver.Request):
    if hwebserver.isInDebugMode():
        dt = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        method = request.method()
        path = request.path()
        print("{} <\033[35m{}\033[0m> [\033[4;34m{}\033[0m]".format(dt, method.upper(), path))


@hwebserver.urlHandler("/api/hdalibrary")
def hdalibrary(request: hwebserver.Request):
    logRequestDebugInfo(request)
    hdas = os.listdir("HDALibrary")
    hdaLibrary = {}
    for hdaFile in hdas:
        if '.hda' not in hdaFile:
            continue
        hdaPath = os.path.join("HDALibrary", hdaFile)
        definition = hou.hda.definitionsInFile(hdaPath)[0]
        if not definition.isInstalled():
            hou.hda.installFile(hdaPath)
        nodeType = definition.nodeTypeCategory().name()
        if nodeType not in hdaLibrary:
            hdaLibrary[nodeType] = {}
        hdaLibrary[nodeType][hdaFile] = definition.description()
    return hwebserver.Response(json.dumps(hdaLibrary, indent=4), content_type="application/json;charset=utf-8")


@hwebserver.urlHandler("/api/hdaprocessor/", is_prefix=True)
def hdaprocessor(request: hwebserver.Request):
    hdaPath = os.path.abspath(os.path.join("HDALibrary", os.path.basename(request.path())))
    if request.method() == "POST":
        return hdaprocessor_post(hdaPath, request)
    else:
        return hdaprocessor_get(hdaPath, request)


def hdaprocessor_post(hdaPath, request: hwebserver.Request):
    hou.hipFile.save("temp/project.hiplc")
    print(hou.hipFile.path())
    logRequestDebugInfo(request)
    formData = request.POST()
    files = request.files()
    definition = hou.hda.definitionsInFile(hdaPath)[0]
    if not definition.isInstalled():
        hou.hda.installFile(hdaPath)
    else:
        hou.hda.reloadFile(hdaPath)
    nodeTypeName = definition.nodeTypeName()
    topnet = hou.node("/tasks").createNode("topnet")
    topNode = topnet.createNode(nodeTypeName)
    fillHDAParm(topNode, formData, files)
    partition = topnet.createNode("partitionbyexpression")
    partition.setFirstInput(topNode)
    fileCompress = topnet.createNode("filecompress")
    fileCompress.setFirstInput(partition)
    HARPOON_ROOT = hou.getenv("HARPOON_ROOT")
    print(HARPOON_ROOT)
    topOutputFile = os.path.join(HARPOON_ROOT, r"temp\output\output.zip")
    fileCompress.parm("output_filename").set(topOutputFile)
    hou.hipFile.save("temp/project.hiplc")
    fileCompress.executeGraph(filter_static=False, block=True, generate_only=False, tops_only=False)
    responseFile = os.path.join(HARPOON_ROOT, r"temp\response.zip")
    shutil.copy(topOutputFile, responseFile)
    topNode.dirtyWorkItems(True)
    topnet.destroy()
    response = hwebserver.fileResponse(responseFile, delete_file=True)
    response.setHeader("file-name", "result.zip")
    return response


def fillHDAParm(node: hou.Node, formData, files):
    for parm, value in formData.items():
        values = json.loads(value)
        if not isinstance(values, str):
            values = tuple(values) if (len(values) > 1) else values[0]
        node.setParms({parm: values})
    for parm, file in files.items():
        file.saveToDisk()
        HARPOON_ROOT = hou.getenv("HARPOON_ROOT")
        tmpFilePath = file.temporaryFilePath()
        tmpFileName = os.path.basename(tmpFilePath)
        filePath = os.path.join(HARPOON_ROOT, "temp", tmpFileName)
        shutil.copy(tmpFilePath, filePath)
        node.parm(parm).set(filePath)


def hdaprocessor_get(hdaPath, request: hwebserver.Request):
    logRequestDebugInfo(request)
    definition = hou.hda.definitionsInFile(hdaPath)[0]
    if not definition.isInstalled():
        hou.hda.installFile(hdaPath)
    jsonObj = definition.toJson()
    return hwebserver.Response(json.dumps(jsonObj, indent=4), content_type="application/json;charset=utf-8")
