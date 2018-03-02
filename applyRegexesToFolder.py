import applyRegexToFolder as Apply
import shutil

#inputFolder = 'test'
outputFolder = r'C:\Work\Source\composer\src\nodemodels'

#shutil.rmtree(outputFolder, True)
#shutil.copytree(inputFolder, outputFolder)

Apply.setExtensionFilter(['cpp', 'hpp', 'h', 'c'])

#Apply.setParameters(outputFolder, outputFolder, r'#include "' + className + '"', r'#include <common/' + className + '.hpp>')
#Apply.run()

#flow
#['Connection', 'DataModelRegistry', 'Graph', 'Node', 'NodeData', 'NodeDataModel', 'NodeInput', 'NodeModelBase', 'NodeOutput', 'NodeState', 'PortType']
#nodeeditor
#['ConnectionBlurEffect', 'ConnectionGeometry', 'ConnectionGraphicsObject', 'ConnectionPainter', 'ConnectionState', 'ConnectionStyle', 'Export', 'FlowScene', 'FlowView', 'FlowViewDragHelper', 'FlowViewStyle', 'NodeConnectionInteraction', 'NodeGeometry', 'NodeGraphics', 'NodeGraphics_ViewFrameworkImpl', 'NodePainter', 'NodePainterDelegate', 'NodeStyle', 'Properties', 'Style', 'StyleCollection']


for className in ['ConnectionBlurEffect']:
	#Apply.setParameters(outputFolder, outputFolder, r'([^a-zA-Z/])' + className + r'([^a-zA-Z\.])', r'\1QtNodes::' + className + r'\2')
	#Apply.run()
	
	Apply.setParameters(outputFolder, outputFolder, r'NodeWidgetStyle::addStyle\((.*)\)', r'\1')
	Apply.run()
