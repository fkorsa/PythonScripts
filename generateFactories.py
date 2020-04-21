import os
import sys
import shutil
import re
import fileUtils
from stringUtils import *
import generateManagerFactory
import addFunctionWrappers

inputFolder = sys.argv[1]
animationManagerFilePath = sys.argv[2]

defaultNames = dict()
defaultNames["camera_dof"] = "DOF"
defaultNames["camera_path"] = "Path"
defaultNames["camera_switch_event"] = "Camera Switch Event"
defaultNames["camera_twist"] = "Camera Twist"
defaultNames["camera_zoom"] = "Camera Zoom"
defaultNames["day_arc"] = "Sun & Sky Day Arc"
defaultNames["deformable"] = "Deformable"
defaultNames["dolly"] = "Dolly"
defaultNames["environment_rotation"] = "Environment Rotation"
defaultNames["fade"] = "Fade"
defaultNames["fbx"] = "FBX"
defaultNames["hide_event"] = "Hide Event"
defaultNames["inclination"] = "Inclination"
defaultNames["material"] = "Material"
defaultNames["orbit"] = "Orbit"
defaultNames["panorama"] = "Panorama"
defaultNames["rotation"] = "Rotation"
defaultNames["studio_switch_event"] = "Studio Switch Event"
defaultNames["translation"] = "Translation"
defaultNames["turntable"] = "Turntable"
defaultNames["vr"] = "VR"
defaultNames["vr_camera"] = "KeyShotXR Camera"
defaultNames["vr_object"] = "VR Object"

enumNames = dict()
enumNames["camera_dof"] = "CameraDOF"
enumNames["camera_path"] = "CameraPath"
enumNames["camera_switch_event"] = "CameraSwitch"
enumNames["camera_twist"] = "CameraTwist"
enumNames["camera_zoom"] = "CameraZoom"
enumNames["day_arc"] = "SunSkyDayArc"
enumNames["deformable"] = "Deformable"
enumNames["dolly"] = "CameraDolly"
enumNames["environment_rotation"] = "EnvironmentRotation"
enumNames["fade"] = "Fade"
enumNames["fbx"] = "FBX"
enumNames["hide_event"] = "HideEvent"
enumNames["inclination"] = "CameraInclination"
enumNames["material"] = "Material"
enumNames["orbit"] = "CameraOrbit"
enumNames["panorama"] = "CameraPanorama"
enumNames["rotation"] = "Rotation"
enumNames["studio_switch_event"] = "StudioSwitch"
enumNames["translation"] = "Translation"
enumNames["turntable"] = "Turntable"
enumNames["vr"] = "VR"
enumNames["vr_camera"] = "CameraVR"
enumNames["vr_object"] = "VR"

noAnimationNodeParameter = ["CameraEvent", "Zoom", "StudioSwitch", "CameraEvent"]

propertiesNames = dict()
propertiesNames["camera_dof"] = ["Dof"]
propertiesNames["camera_switch_event"] = ["CameraEvent"]
propertiesNames["camera_path"] = ["CameraPath", "PickTarget"]
propertiesNames["camera_twist"] = ["Rotation"]
propertiesNames["deformable"] = []
propertiesNames["camera_zoom"] = ["Zoom"]
propertiesNames["dolly"] = []
propertiesNames["environment_rotation"] = ["Rotation"]
propertiesNames["fbx"] = []
propertiesNames["hide_event"] = []
propertiesNames["fade"] = ["Fade"]
propertiesNames["inclination"] = ["Rotation"]
propertiesNames["turntable"] = ["Rotation"]
propertiesNames["vr"] = []
propertiesNames["studio_switch_event"] = ["StudioSwitch"]
propertiesNames["vr_camera"] = []
propertiesNames["panorama"] = ["Rotation"]
propertiesNames["vr_object"] = []
propertiesNames["orbit"] = ["Rotation"]
propertiesNames["material"] = []
propertiesNames["rotation"] = ["Rotation", "PickPivot"]
propertiesNames["translation"] = ["Translation"]

daliNames = dict()
daliNames["camera_dof"] = "camera_dof"
daliNames["camera_switch_event"] = "camera_switch_event"
daliNames["camera_path"] = "camera_path"
daliNames["camera_twist"] = "camera_twist"
daliNames["deformable"] = "deformable"
daliNames["camera_zoom"] = "camera_zoom"
daliNames["dolly"] = "dolly"
daliNames["environment_rotation"] = "env_rotate"
daliNames["fbx"] = "fbx_animation"
daliNames["hide_event"] = "hide_event"
daliNames["fade"] = "fade"
daliNames["inclination"] = "inclination"
daliNames["turntable"] = "turntable"
daliNames["vr"] = "vr"
daliNames["studio_switch_event"] = "studio_switch_event"
daliNames["vr_camera"] = "vr_camera"
daliNames["panorama"] = "panorama"
daliNames["vr_object"] = "vr_object"
daliNames["orbit"] = "orbit"
daliNames["material"] = "material"
daliNames["rotation"] = "rotation"
daliNames["translation"] = "translation"

targetNames = dict()
targetNames["camera_dof"] = "Camera"
targetNames["camera_switch_event"] = "Camera"
targetNames["camera_path"] = "Camera"
targetNames["camera_twist"] = "Camera"
targetNames["deformable"] = "Geometry"
targetNames["camera_zoom"] = "Camera"
targetNames["dolly"] = "Camera"
targetNames["environment_rotation"] = "Environment"
targetNames["fbx"] = "Other"
targetNames["hide_event"] = "Geometry"
targetNames["fade"] = "Geometry"
targetNames["inclination"] = "Camera"
targetNames["turntable"] = "Geometry"
targetNames["vr"] = "Other"
targetNames["studio_switch_event"] = "Studio"
targetNames["vr_camera"] = "Camera"
targetNames["panorama"] = "Camera"
targetNames["vr_object"] = "Geometry"
targetNames["orbit"] = "Camera"
targetNames["material"] = "Material"
targetNames["rotation"] = "Geometry"
targetNames["translation"] = "Geometry"


class FileChanger(fileUtils.FileChanger):
    def __init__(self, snakeCaseName, capitalizedName):
        self.snakeCaseName = snakeCaseName
        self.capitalizedName = capitalizedName

    def changeContents(self, contents):
        snakeCaseName = self.snakeCaseName
        capitalizedName = self.capitalizedName
        if snakeCaseName in ['camera_switch_event', 'studio_switch_event']:
            contents = re.sub(r'KTimelineFlatPainter', 'KTimelineCirclePainter', contents)
        contents = re.sub(r'\("env_sky_time", KAnimationTarget::SunSky\)',
                          '("' + daliNames[snakeCaseName] + '", KAnimationTarget::' + targetNames[snakeCaseName] + ')',
                          contents)
        contents = re.sub(r'DAYARC', capitalizedName.upper(), contents)
        contents = re.sub(r'tr\("Sun & Sky Day Arc"\)', 'tr("' + defaultNames[snakeCaseName] + '")', contents)
        contents = re.sub(r'tr\("Sun && Sky Day Arc"\)', 'tr("' + defaultNames[snakeCaseName] + '")', contents)
        contents = re.sub(r'KAnimationType::SunSkyDayArc', 'KAnimationType::' + enumNames[snakeCaseName], contents)
        if snakeCaseName in propertiesNames:
            includeString = ''
            for propertyName in propertiesNames[snakeCaseName]:
                includeString += '#include "animation/propertywidgets/K' + propertyName + 'PropertiesWidget.h"\n'
            contents = re.sub(r'#include "animation/propertywidgets/KDayArcPropertiesWidget.h"\n', includeString,
                              contents)
            widgetsString = ''
            index = 0
            for propertyName in propertiesNames[snakeCaseName]:
                if propertyName == "Fade":
                    widgetsString += 'new KFadePropertiesWidget(animationEdit, parameters->fade_from_parm, parameters->fade_to_parm)'
                else:
                    widgetsString += 'new K' + propertyName + 'PropertiesWidget(animationEdit, parameters'
                    if propertyName not in noAnimationNodeParameter:
                        widgetsString += ', animationNode'
                    widgetsString += ')'
                if index < len(propertiesNames[snakeCaseName]) - 1:
                    widgetsString += ', '
            contents = re.sub(r'return {new KDayArcPropertiesWidget\(animationEdit, parameters, animationNode\)};',
                              'return {' + widgetsString + '};', contents)
        contents = re.sub(r'day_arc', snakeCaseName, contents)
        contents = re.sub(r'DAY_ARC', snakeCaseName.upper(), contents)
        contents = re.sub(r'DayArc', capitalizedName, contents)
        camelCaseName = capitalizedName[0].lower() + capitalizedName[1:]
        contents = re.sub(r'dayArc', camelCaseName, contents)
        return contents


def getSuffixes():
    suffixes = []
    for _, _, filenames in os.walk(os.path.join(inputFolder, 'day_arc')):
        for filename in filenames:
            if filename.endswith('.cc'):
                suffixes.append(filename[7:-3])
            else:
                suffixes.append(filename[7:-2])
    return set(suffixes)


def fillDirectory(dirname, suffixes):
    for suffix in suffixes:
        snakeCaseName = 'day_arc'
        animationName = capitalize(snakeCaseName)
        baseName = toFileName(animationName, suffix)
        inputHeader = os.path.join(inputFolder, snakeCaseName, baseName + '.h')
        inputImpl = os.path.join(inputFolder, snakeCaseName, baseName + '.cc')
        animationName = capitalize(dirname)
        baseName = toFileName(animationName, suffix)

        headerPath = os.path.join(inputFolder, dirname, baseName + '.h')
        implPath = os.path.join(inputFolder, dirname, baseName + '.cc')

        shutil.copyfile(inputHeader, headerPath)
        shutil.copyfile(inputImpl, implPath)

        fileChanger = FileChanger(dirname, animationName)
        fileChanger.run(headerPath)
        fileChanger = FileChanger(dirname, animationName)
        fileChanger.run(implPath)

        addFunctionWrappers.add(headerPath)
        addFunctionWrappers.add(implPath)

        print('  animation/types/' + dirname + '/' + baseName + '.h')
        print('  animation/types/' + dirname + '/' + baseName + '.cc')


def fillDirectories(suffixes):
    animationTypes = []
    for _, dirnames, filenames in os.walk(inputFolder):
        for dirname in dirnames:
            animationTypes.append(dirname)
            if dirname != 'day_arc':
                fillDirectory(dirname, suffixes)
    return animationTypes


suffixes = getSuffixes()
animationTypes = fillDirectories(suffixes)
generateManagerFactory.generate(animationTypes, animationManagerFilePath)
