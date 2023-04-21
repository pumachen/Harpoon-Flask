from typing import Dict, Any
import hou
import json


def nodeToJson(node: hou.Node):
    jsonObj = {
        'inputNames': node.inputNames(),
        'inputLabels': node.inputLabels(),
        'outputNames': node.outputNames(),
        'outputLabels': node.outputLabels(),
    }
    return jsonObj


def nodeTypeToJson(nodeType: hou.NodeType):
    jsonObj = {
        'name': nodeType.name(),
        'description': nodeType.description(),
        'sourcePath': nodeType.sourcePath(),
        'sourceNetwork': (nodeType.sourceNetwork())
    }
    return jsonObj


def HDADefinitionToJson(definition: hou.HDADefinition):
    jsonObj = {
        'nodeType': nodeTypeToJson(definition.nodeType()),
        'nodeTypeCategory': str(definition.nodeTypeCategory().name()),
        'nodeTypeName': definition.nodeTypeName(),
        'libraryFilePath': definition.libraryFilePath(),
        'isInstalled': definition.isInstalled(),
        'version': definition.version(),
        'comment': definition.comment(),
        'description': definition.description(),
        'icon': definition.icon(),
        'modificationTime': definition.modificationTime(),
        'embeddedHelp': definition.embeddedHelp(),
        'userInfo': definition.userInfo(),
        'extraInfo': definition.extraInfo(),
        'minNumInputs': definition.minNumInputs(),
        'maxNumInputs': definition.maxNumInputs(),
        'maxNumOutputs': definition.maxNumOutputs(),
        'parmTemplateGroup': definition.parmTemplateGroup().toJson()
    }
    return jsonObj


def ParmTemplateGroupToJson(parmTemplateGroup: hou.ParmTemplateGroup):
    parmTemplates = []
    for parmTemplate in parmTemplateGroup.entries():
        parmTemplates.append(parmTemplate.toJson())
    jsonObj = {
        'name': parmTemplateGroup.name(),
        'label': parmTemplateGroup.label(),
        'parmTemplates': parmTemplates
    }
    return jsonObj


def ParmTemplateToJson(parmTemplate: hou.ParmTemplate):
    jsonObj: dict[str, Any] = {}
    jsonObj['name'] = parmTemplate.name()
    jsonObj['label'] = parmTemplate.label()
    jsonObj['type'] = str(parmTemplate.type()).split(".")[1]
    jsonObj['dataType'] = str(parmTemplate.dataType()).split(".")[1]
    jsonObj['numComponents'] = parmTemplate.numComponents()
    # jsonObj['namingScheme'] = str(parmTemplate.namingScheme())
    jsonObj['look'] = str(parmTemplate.look()).split(".")[1]
    jsonObj['help'] = parmTemplate.help()
    jsonObj['isHidden'] = parmTemplate.isHidden()
    jsonObj['isLabelHidden'] = parmTemplate.isLabelHidden()
    jsonObj['joinsWithNext'] = parmTemplate.joinsWithNext()
    # jsonObj['disableWhen'] = str(parmTemplate.disableWhen())
    # jsonObj['conditionals'] = parmTemplate.conditionals()
    jsonObj['tags'] = parmTemplate.tags()
    # jsonObj['scriptCallback'] = parmTemplate.scriptCallback()
    # jsonObj['scriptCallbackLanguage'] = str(parmTemplate.scriptCallbackLanguage())
    return jsonObj


def IntParmTemplateToJson(intParmTemplate: hou.IntParmTemplate):
    jsonObj = ParmTemplateToJson(intParmTemplate)
    jsonObj['defaultValue'] = intParmTemplate.defaultValue()
    # jsonObj['defaultExpression'] = intParmTemplate.defaultExpression()
    # jsonObj['defaultExpressionLanguage'] = str(intParmTemplate.defaultExpressionLanguage())
    jsonObj['minValue'] = intParmTemplate.minValue()
    jsonObj['maxValue'] = intParmTemplate.maxValue()
    jsonObj['minIsStrict'] = intParmTemplate.minIsStrict()
    jsonObj['maxIsStrict'] = intParmTemplate.maxIsStrict()
    jsonObj['menuItems'] = intParmTemplate.menuItems()
    jsonObj['menuLabels'] = intParmTemplate.menuLabels()
    jsonObj['iconNames'] = intParmTemplate.iconNames()
    # jsonObj['itemGeneratorScript'] = intParmTemplate.itemGeneratorScript()
    # jsonObj['itemGeneratorScriptLanguage'] = str(intParmTemplate.itemGeneratorScriptLanguage())
    jsonObj['menuType'] = str(intParmTemplate.menuType()).split(".")[1]
    jsonObj['menuUseToken'] = intParmTemplate.menuUseToken()
    return jsonObj


def FloatParmTemplateToJson(floatParmTemplate: hou.FloatParmTemplate):
    jsonObj = ParmTemplateToJson(floatParmTemplate)
    jsonObj['defaultValue'] = floatParmTemplate.defaultValue()
    # jsonObj['defaultExpression'] = floatParmTemplate.defaultExpression()
    # jsonObj['defaultExpressionLanguage'] = str(floatParmTemplate.defaultExpressionLanguage())
    jsonObj['minValue'] = floatParmTemplate.minValue()
    jsonObj['maxValue'] = floatParmTemplate.maxValue()
    jsonObj['minIsStrict'] = floatParmTemplate.minIsStrict()
    jsonObj['maxIsStrict'] = floatParmTemplate.maxIsStrict()
    return jsonObj


def StringParmTemplateToJson(stringParmTemplate: hou.StringParmTemplate):
    jsonObj = ParmTemplateToJson(stringParmTemplate)
    jsonObj['defaultValue'] = stringParmTemplate.defaultValue()
    # jsonObj['defaultExpression'] = stringParmTemplate.defaultExpression()
    # jsonObj['defaultExpressionLanguage'] = str(stringParmTemplate.defaultExpressionLanguage())
    jsonObj['stringType'] = str(stringParmTemplate.stringType()).split(".")[1]
    jsonObj['fileType'] = str(stringParmTemplate.fileType()).split(".")[1]
    jsonObj['menuItems'] = stringParmTemplate.menuItems()
    jsonObj['menuLabels'] = stringParmTemplate.menuLabels()
    # jsonObj['iconNames'] = stringParmTemplate.iconNames()
    # jsonObj['itemGeneratorScript'] = stringParmTemplate.itemGeneratorScript()
    # jsonObj['itemGeneratorScriptLanguage'] = str(stringParmTemplate.itemGeneratorScriptLanguage())
    jsonObj['menuType'] = str(stringParmTemplate.menuType()).split(".")[1]
    return jsonObj


def ToggleParmTemplateToJson(toggleParmTemplate: hou.ToggleParmTemplate):
    jsonObj = ParmTemplateToJson(toggleParmTemplate)
    jsonObj['defaultValue'] = toggleParmTemplate.defaultValue()
    # jsonObj['defaultExpression'] = toggleParmTemplate.defaultExpression()
    # jsonObj['defaultExpressionLanguage'] = str(toggleParmTemplate.defaultExpressionLanguage())
    return jsonObj


def MenuParmTemplateToJson(menuParmTemplate: hou.MenuParmTemplate):
    jsonObj = ParmTemplateToJson(menuParmTemplate)
    jsonObj['menuItems'] = menuParmTemplate.menuItems()
    jsonObj['menuLabels'] = menuParmTemplate.menuLabels()
    jsonObj['defaultValue'] = menuParmTemplate.defaultValue()
    jsonObj['defaultValueAsString'] = menuParmTemplate.defaultValueAsString()
    # jsonObj['defaultExpression'] = menuParmTemplate.defaultExpression()
    # jsonObj['defaultExpressionLanguage'] = str(menuParmTemplate.defaultExpressionLanguage())
    # jsonObj['iconNames'] = menuParmTemplate.iconNames()
    # jsonObj['itemGeneratorScript'] = menuParmTemplate.itemGeneratorScript()
    # jsonObj['itemGeneratorScriptLanguage'] = str(menuParmTemplate.itemGeneratorScriptLanguage())
    jsonObj['menuType'] = str(menuParmTemplate.menuType())
    jsonObj['enuUseToken'] = menuParmTemplate.menuUseToken()
    jsonObj['isMenu'] = menuParmTemplate.isMenu()
    jsonObj['isButtonStrip'] = menuParmTemplate.isButtonStrip()
    jsonObj['isIconStrip'] = menuParmTemplate.isIconStrip()
    return jsonObj


hou.HDADefinition.toJson = HDADefinitionToJson
hou.IntParmTemplate.toJson = IntParmTemplateToJson
hou.FloatParmTemplate.toJson = FloatParmTemplateToJson
hou.StringParmTemplate.toJson = StringParmTemplateToJson
hou.ToggleParmTemplate.toJson = ToggleParmTemplateToJson
hou.MenuParmTemplate.toJson = MenuParmTemplateToJson
hou.ParmTemplate.toJson = ParmTemplateToJson
hou.ParmTemplateGroup.toJson = ParmTemplateGroupToJson


