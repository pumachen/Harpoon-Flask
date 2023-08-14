from __future__ import annotations
from typing import Dict, Any
import hou
import json
from xml.etree import ElementTree
from enum import Enum

class StringParmType(Enum):
    Regular = "Regular"
    FileReference = "FileReference"

class ParmDataType(Enum):
    Int = "Int"
    Float = "Float"
    String = "String"
    Ramp = "Ramp"

class ParmTemplateType(Enum):
    Int = "Int"
    Float = "Float"
    String = "String"
    Toggle = "Toggle"
    Menu = "Menu"
    Button = "Button"
    FolderSet = "FolderSet"
    Folder = "Folder"
    Separator = "Separator"
    Label = "Label"
    Ramp = "Ramp"

class ParmTemplate:
    name: str
    label: str
    type: str
    dataType: str
    numComponents: int
    look = ""
    help = ""
    isHidden = False
    isLabelHidden = False
    joinsWithNext = False

    def serialize(self) -> dict:
        return {
            "name": self.name,
            "label": self.label,
            "type": self.type,
            "dataType": self.dataType,
            "numComponents": self.numComponents,
            "look": self.look,
            "help": self.help,
            "isHidden": self.isHidden,
            "isLabelHidden": self.isLabelHidden,
            "joinsWithNext": self.joinsWithNext
        }

    @classmethod
    def _FromHouParmTemplate(cls, houParmTemplate: hou.ParmTemplate) -> ParmTemplate:
        parmTemplate = cls()
        parmTemplate.name = houParmTemplate.name()
        parmTemplate.label = houParmTemplate.label()
        parmTemplate.type = str(houParmTemplate.type()).split(".")[1]
        parmTemplate.dataType = ParmDataType(str(houParmTemplate.dataType()).split(".")[1]).value
        parmTemplate.numComponents = houParmTemplate.numComponents()
        #parmTemplate.namingScheme = str(parmTemplate.namingScheme())
        parmTemplate.look = str(houParmTemplate.look()).split(".")[1]
        parmTemplate.help = houParmTemplate.help()
        parmTemplate.isHidden = houParmTemplate.isHidden()
        parmTemplate.isLabelHidden = houParmTemplate.isLabelHidden()
        parmTemplate.joinsWithNext = houParmTemplate.joinsWithNext()
        #parmTemplate.disableWhen = str(parmTemplate.disableWhen())
        #parmTemplate.conditionals = parmTemplate.conditionals()
        return parmTemplate

    torTypeToParmType = {
        "int": "Int",
        "choice": "Int",
        "double": "Float",
        "bool": "Toggle",
        "in": "String",
        "out": "String"
    }
    torTypeToParmDataType = {
        "int": "Int",
        "choice": "Int",
        "double": "Float",
        "bool": "Toggle",
        "in": "String",
        "out": "String"
    }

    @classmethod
    def _FromTorParmTemplate(cls, torParmTemplate: ElementTree.Element) -> ParmTemplate:
        parmTemplate = cls()
        parmTemplate.name = torParmTemplate.get("Variable")
        parmTemplate.label = "{0}:{1}".format(torParmTemplate.get("Owner"), torParmTemplate.get("Name"))
        torType = torParmTemplate.get("Type")
        parmTemplate.type = parmTemplate.torTypeToParmType[torType]
        parmTemplate.dataType = parmTemplate.torTypeToParmDataType[torType]
        parmTemplate.numComponents = 1
        parmTemplate.look = "Regular"
        return parmTemplate

class IntParmTemplate(ParmTemplate):
    defaultValue: []
    minValue: int
    maxValue: int
    minIsStrict = False
    maxIsStrict = False
    menuItems = []
    menuLabels = []

    def serialize(self) -> dict:
        table = ParmTemplate.serialize(self)
        table["defaultValue"] = self.defaultValue
        table["minValue"] = self.minValue
        table["maxValue"] = self.maxValue
        table["minIsStrict"] = self.minIsStrict
        table["maxIsStrict"] = self.maxIsStrict
        table["menuItems"] = self.menuItems
        table["menuLabels"] = self.menuLabels
        return table

    @classmethod
    def FromHouIntParmTemplate(cls, houIntParmTemplate: hou.IntParmTemplate) -> IntParmTemplate:
        intParmTemplate: IntParmTemplate = IntParmTemplate._FromHouParmTemplate(houIntParmTemplate)
        intParmTemplate.defaultValue = houIntParmTemplate.defaultValue()
        intParmTemplate.minValue = houIntParmTemplate.minValue()
        intParmTemplate.maxValue = houIntParmTemplate.maxValue()
        intParmTemplate.minIsStrict = houIntParmTemplate.minIsStrict()
        intParmTemplate.maxIsStrict = houIntParmTemplate.maxIsStrict()
        intParmTemplate.menuItems = houIntParmTemplate.menuItems()
        intParmTemplate.menuLabels = houIntParmTemplate.menuLabels()
        return intParmTemplate

    @classmethod
    def FromTorIntParmTemplate(cls, torIntParmTemplate: ElementTree.Element) -> IntParmTemplate:
        intParmTemplate: IntParmTemplate = IntParmTemplate._FromTorParmTemplate(torIntParmTemplate)
        intParmTemplate.defaultValue = [ torIntParmTemplate.get("Default") ]
        intParmTemplate.minValue = torIntParmTemplate.get("Min")
        intParmTemplate.maxValue = torIntParmTemplate.get("Max")
        intParmTemplate.minIsStrict = True
        intParmTemplate.maxIsStrict = True
        if torIntParmTemplate.get("Type") == "choice":
            intParmTemplate.menuLabels = torIntParmTemplate.get("Choices").split(",")
            intParmTemplate.menuItems = [ *range(0, len(intParmTemplate.menuLabels)) ]
        return intParmTemplate

class FloatParmTemplate(ParmTemplate):
    defaultValue: []
    minValue: float
    maxValue: float
    minIsStrict = False
    maxIsStrict = False

    def serialize(self) -> dict:
        table = ParmTemplate.serialize(self)
        table["defaultValue"] = self.defaultValue
        table["minValue"] = self.minValue
        table["maxValue"] = self.maxValue
        table["minIsStrict"] = self.minIsStrict
        table["maxIsStrict"] = self.maxIsStrict
        return table

    @classmethod
    def FromHouFloatParmTemplate(cls, houFloatParmTemplate: hou.FloatParmTemplate) -> FloatParmTemplate:
        floatParmTemplate: FloatParmTemplate = FloatParmTemplate._FromHouParmTemplate(houFloatParmTemplate)
        floatParmTemplate.defaultValue = houFloatParmTemplate.defaultValue()
        floatParmTemplate.minValue = houFloatParmTemplate.minValue()
        floatParmTemplate.maxValue = houFloatParmTemplate.maxValue()
        floatParmTemplate.minIsStrict = houFloatParmTemplate.minIsStrict()
        floatParmTemplate.maxIsStrict = houFloatParmTemplate.maxIsStrict()
        return floatParmTemplate

    @classmethod
    def FromTorFloatParmTemplate(cls, torFloatParmTemplate: ElementTree.Element) -> FloatParmTemplate:
        floatParmTemplate: FloatParmTemplate = FloatParmTemplate._FromTorParmTemplate(torFloatParmTemplate)
        floatParmTemplate.defaultValue = [ torFloatParmTemplate.get("Default") ]
        floatParmTemplate.minValue = torFloatParmTemplate.get("Min")
        floatParmTemplate.maxValue = torFloatParmTemplate.get("Max")
        floatParmTemplate.minIsStrict = True
        floatParmTemplate.maxIsStrict = True
        return floatParmTemplate

class StringParmTemplate(ParmTemplate):
    defaultValue: []
    stringType: str
    fileType = ""
    menuItems = []
    menuLabels = []

    def serialize(self) -> dict:
        table = ParmTemplate.serialize(self)
        table["defaultValue"] = self.defaultValue
        table["stringType"] = self.stringType
        table["fileType"] = self.fileType
        table["menuItems"] = self.menuItems
        table["menuLabels"] = self.menuLabels
        return table

    @classmethod
    def FromHouStringParmTemplate(cls, houStringParmTemplate: hou.StringParmTemplate) -> StringParmTemplate:
        stringParmTemplate: StringParmTemplate = StringParmTemplate._FromHouParmTemplate(houStringParmTemplate)
        stringParmTemplate.defaultValue = houStringParmTemplate.defaultValue()
        stringParmTemplate.stringType = str(houStringParmTemplate.stringType()).split(".")[1]
        stringParmTemplate.fileType = str(houStringParmTemplate.fileType()).split(".")[1]
        stringParmTemplate.menuItems = houStringParmTemplate.menuItems()
        stringParmTemplate.menuLabels = houStringParmTemplate.menuLabels()
        return stringParmTemplate

    @classmethod
    def FromTorStringParmTemplate(cls, torStringParmTemplate: ElementTree.Element) -> StringParmTemplate:
        stringParmTemplate: StringParmTemplate = StringParmTemplate._FromTorParmTemplate(torStringParmTemplate)
        stringParmTemplate.defaultValue = [ torStringParmTemplate.get("Default") ]
        stringParmTemplate.stringType = StringParmType.FileReference.value
        stringParmTemplate.fileType = "Image"
        if torStringParmTemplate.get("Type") == "out":
            stringParmTemplate.isHidden = True
        return stringParmTemplate

class ToggleParmTemplate(ParmTemplate):
    defaultValue: []

    def serialize(self) -> dict:
        table = ParmTemplate.serialize(self)
        table["defaultValue"] = self.defaultValue
        return table

    @classmethod
    def FromHouToggleParmTemplate(cls, houToggleParmTemplate: hou.ToggleParmTemplate) -> ToggleParmTemplate:
        toggleParmTemplate: ToggleParmTemplate = ToggleParmTemplate._FromHouParmTemplate(houToggleParmTemplate)
        toggleParmTemplate.defaultValue = houToggleParmTemplate.defaultValue()
        return toggleParmTemplate

    @classmethod
    def FromTorToggleParmTemplate(cls, torToggleParmTemplate: ElementTree.Element) -> ToggleParmTemplate:
        toggleParmTemplate: ToggleParmTemplate = ToggleParmTemplate._FromTorParmTemplate(torToggleParmTemplate)
        toggleParmTemplate.defaultValue = [ torToggleParmTemplate.get("Default") ]
        return toggleParmTemplate

class MenuParmTemplate(ParmTemplate):
    defaultValue: []
    defaultValueAsString: bool
    menuItems: []
    menuLabels: []
    menuType: str
    isMenu: bool
    isButtonStrip: bool
    isIconStrip: bool

    def serialize(self) -> dict:
        table = ParmTemplate.serialize(self)
        table["defaultValue"] = self.defaultValue
        table["defaultValueAsString"] = self.defaultValueAsString
        table["menuItems"] = self.menuItems
        table["menuLabels"] = self.menuLabels
        table["menuType"] = self.menuType
        table["isMenu"] = self.isMenu
        table["isButtonStrip"] = self.isButtonStrip
        table["isIconStrip"] = self.isButtonStrip
        return table

    @classmethod
    def FromHouMenuParmTemplate(cls, houMenuParmTemplate: hou.MenuParmTemplate) -> MenuParmTemplate:
        menuParmTemplate: MenuParmTemplate = MenuParmTemplate._FromHouParmTemplate(houMenuParmTemplate)
        menuParmTemplate.menuItems = houMenuParmTemplate.menuItems()
        menuParmTemplate.menuLabels = houMenuParmTemplate.menuLabels()
        menuParmTemplate.defaultValue = houMenuParmTemplate.defaultValue()
        menuParmTemplate.defaultValueAsString = houMenuParmTemplate.defaultValueAsString()
        menuParmTemplate.menuType = str(houMenuParmTemplate.menuType())
        menuParmTemplate.isMenu = houMenuParmTemplate.isMenu()
        menuParmTemplate.isButtonStrip = houMenuParmTemplate.isButtonStrip()
        menuParmTemplate.isIconStrip = houMenuParmTemplate.isIconStrip()
        return menuParmTemplate

class ParmTemplateGroup:
    name = ""
    label = ""
    parmTemplates = [ParmTemplate]

    def serialize(self) -> dict:
        parmTemplates = []
        for parmTemplate in self.parmTemplates:
            parmTemplates.append(parmTemplate.serialize())
        return {
            "name": self.name,
            "label": self.label,
            "parmTemplates": parmTemplates
        }

    @classmethod
    def FromHouParmTemplateGroup(cls, houParmTemplateGroup: hou.ParmTemplateGroup) -> ParmTemplateGroup:
        parmTemplates = []
        for houParmTemplate in houParmTemplateGroup.entries():
            type = houParmTemplate.type()
            parmTemplate = None
            if type == hou.parmTemplateType.Int:
                parmTemplate = IntParmTemplate.FromHouIntParmTemplate(houParmTemplate)
            elif type == hou.parmTemplateType.Float:
                parmTemplate = FloatParmTemplate.FromHouFloatParmTemplate(houParmTemplate)
            elif type == hou.parmTemplateType.String:
                parmTemplate = StringParmTemplate.FromHouStringParmTemplate(houParmTemplate)
            elif type == hou.parmTemplateType.Toggle:
                parmTemplate = ToggleParmTemplate.FromHouToggleParmTemplate(houParmTemplate)
            elif type == hou.parmTemplateType.Menu:
                parmTemplate = MenuParmTemplate.FromHouMenuParmTemplate(houParmTemplate)
            if parmTemplate is None:
                print(type)
            else:
                parmTemplates.append(parmTemplate)
        parmTemplateGroup = cls()
        parmTemplateGroup.name = houParmTemplateGroup.name()
        parmTemplateGroup.label = houParmTemplateGroup.label()
        parmTemplateGroup.parmTemplates = parmTemplates
        return parmTemplateGroup

    @classmethod
    def FromTorNodeMap(cls, torNodeMap: ElementTree) -> ParmTemplateGroup:
        parmTemplateGroup = cls()
        parmTemplates = []
        for torParmTemplate in torNodeMap.findall("Parameter"):
            type = torParmTemplate.get("Type")
            parmTemplate = None
            if type in ["int", "choice"]:
                parmTemplate = IntParmTemplate.FromTorIntParmTemplate(torParmTemplate)
            elif type == "double":
                parmTemplate = FloatParmTemplate.FromTorFloatParmTemplate(torParmTemplate)
            elif type in ["in", "out"]:
                parmTemplate = StringParmTemplate.FromTorStringParmTemplate(torParmTemplate)
            elif type == "bool":
                parmTemplate = ToggleParmTemplate.FromTorToggleParmTemplate(torParmTemplate)
            if parmTemplate is not None:
                parmTemplates.append(parmTemplate)
        parmTemplateGroup.parmTemplates = parmTemplates
        return parmTemplateGroup

class HDADefinition:
    nodeType: str
    nodeTypeCategory: str
    nodeTypeName: str
    libraryFilePath: str
    isInstalled: bool
    version: str
    comment: str
    description: str
    icon: str
    modificationTime: int
    embeddedHelp: str
    userInfo: str
    extraInfo: str
    minNumInputs: int
    maxNumInputs: int
    maxNumOutputs: int
    parmTemplateGroup: ParmTemplateGroup

    def serialize(self) -> dict:
        return {
            "nodeType": self.nodeType,
            "nodeTypeCategory": self.nodeTypeCategory,
            "nodeTypeName": self.nodeTypeName,
            "libraryFilePath": self.libraryFilePath,
            "isInstalled": self.isInstalled,
            "version": self.version,
            "comment": self.comment,
            "description": self.description,
            "icon": self.icon,
            "modificationTime": self.modificationTime,
            "embeddedHelp": self.embeddedHelp,
            "userInfo": self.userInfo,
            "extraInfo": self.extraInfo,
            "minNumInputs": self.minNumInputs,
            "maxNumInputs": self.maxNumInputs,
            "maxNumOutputs": self.maxNumOutputs,
            "parmTemplateGroup": self.parmTemplateGroup.serialize(),
        }

    def __init__(self, definition: hou.HDADefinition):
        self.nodeType = nodeTypeToJson(definition.nodeType())
        self.nodeTypeCategory = str(definition.nodeTypeCategory().name())
        self.nodeTypeName = definition.nodeTypeName()
        self.libraryFilePath = definition.libraryFilePath()
        self.isInstalled = definition.isInstalled()
        self.version = definition.version()
        self.comment = definition.comment()
        self.description = definition.description()
        self.icon = definition.icon()
        self.modificationTime = definition.modificationTime()
        self.embeddedHelp = definition.embeddedHelp()
        self.userInfo = definition.userInfo()
        self.extraInfo = definition.extraInfo()
        self.minNumInputs = definition.minNumInputs()
        self.maxNumInputs = definition.maxNumInputs()
        self.maxNumOutputs = definition.maxNumOutputs()
        self.parmTemplateGroup = ParmTemplateGroup.FromHouParmTemplateGroup(definition.parmTemplateGroup())

def nodeToJson(node: hou.Node):
    return {
        'inputNames': node.inputNames(),
        'inputLabels': node.inputLabels(),
        'outputNames': node.outputNames(),
        'outputLabels': node.outputLabels(),
    }

def nodeTypeToJson(nodeType: hou.NodeType):
    return {
        'name': nodeType.name(),
        'description': nodeType.description(),
        'sourcePath': nodeType.sourcePath(),
        'sourceNetwork': (nodeType.sourceNetwork())
    }