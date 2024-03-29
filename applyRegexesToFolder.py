import applyRegexToFolder as Apply
import shutil

#inputFolder = 'test'
outputFolder = r'/Users/luxionkeyshot/work/source/luxion/src'

#shutil.rmtree(outputFolder, True)
#shutil.copytree(inputFolder, outputFolder)

Apply.setExtensionFilter(['cpp', 'hpp', 'h', 'c', 'cc'])

Apply.setParameters(outputFolder, outputFolder, r'(LUX_(SVG_)?ICON)\("([^"]+?)(\.svg)?(\.png)?"\)', r'\1("\3")', False, True)
Apply.run()

#flow
#['Connection', 'DataModelRegistry', 'Graph', 'Node', 'NodeData', 'NodeDataModel', 'NodeInput', 'NodeModelBase', 'NodeOutput', 'NodeState', 'PortType']
#nodeeditor
#['ConnectionBlurEffect', 'ConnectionGeometry', 'ConnectionGraphicsObject', 'ConnectionPainter', 'ConnectionState', 'ConnectionStyle', 'Export', 'FlowScene', 'FlowView', 'FlowViewDragHelper', 'FlowViewStyle', 'NodeConnectionInteraction', 'NodeGeometry', 'NodeGraphics', 'NodeGraphics_ViewFrameworkImpl', 'NodePainter', 'NodePainterDelegate', 'NodeStyle', 'Properties', 'Style', 'StyleCollection']


'''

	(
		{
			{ "Ô",OperatorData().type(), Flow::NodeInput::REQUIRED },
			{ "ψ",StateData().type(), Flow::NodeInput::REQUIRED }
		},
		{ 
			{ "",StateData().type() } 
		}
	)

'''

'''
for className in ['ConnectionBlurEffect']:
	#Apply.setParameters(outputFolder, outputFolder, r'([^a-zA-Z/])' + className + r'([^a-zA-Z\.])', r'\1QtNodes::' + className + r'\2')
	#Apply.run()
	
	Apply.setParameters(outputFolder, outputFolder, r'(Flow::NodeDataModel.*?\t\(.*[^\t\n])(.*?\t\))', r'\1,\n\t\tgraphManager\2', _isDotMatchingAll=True)
	Apply.run()
'''