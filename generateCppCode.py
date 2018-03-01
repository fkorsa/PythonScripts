# Import all dependencies
import re
import os
import sys
import uuid

outputFile = 'code.cpp'


def write_contents(contents):
    file = open(outputFile, 'w')
    file.write(contents)
    file.close()

modelName = 'Potential'
modelUserName = 'Potential'

inputParameters = [
    ['Text', 'expression', 'TextInput'],
]

parameterSet = set()
for param in inputParameters:
	parameterSet.add(param[0])

fullParameterSet = set()
for param in inputParameters:
	fullParameterSet.add(param[2])

'''
for param in parameterSet:
	print('param:' + param)
'''

contents = ''
contents += '// ' + modelName + 'View.hpp\n'
contents += '#pragma once\n\n'
contents += '#include <flow/NodeView.hpp>\n\n'
contents += 'namespace Flow\n'
contents += '{\n'
contents += '	class TextParameter;\n'
contents += '}\n\n'
contents += 'class ' + modelName + 'View : public Flow::NodeView\n'
contents += '{\n'
contents += '	Q_OBJECT\n'
contents += 'public:\n'
contents += '	' + modelName + 'View(Flow::ParameterFactory& parameterFactory);\n\n'
for param in inputParameters:
	contents += '	Flow::' + param[0] + 'Parameter& ' + param[1] + 'Parameter();\n'
if len(inputParameters) > 0:
	contents += '\n'
contents += 'private slots:\n'
for param in inputParameters:
	upperCaseName = param[1][0].upper() + param[1][1:]
	contents += '	void update' + upperCaseName + 'Binding();\n'

contents += '\nprivate:\n'
contents += '	QJsonObject saveModel() const override;\n'
contents += '	void restoreModel(QJsonObject const& json) override;\n\n'
for param in inputParameters:
	upperCaseName = param[1][0].upper() + param[1][1:]
	contents += '	std::unique_ptr<Flow::' + param[0] + 'Parameter> ' + param[1] + 'Parameter_;\n'

contents += '};\n\n\n\n'

contents += '// ' + modelName + 'View.cpp\n'
contents += '#include <main/nodeviews/' + modelName + 'View.hpp>\n\n'

contents += '#include <flow/NodeDataModel.hpp>\n'
contents += '#include <flow/parameters/ParameterFactory.hpp>\n'
for param in parameterSet:
	contents += '#include <flow/parameters/' + param + 'Parameter.hpp>\n'

contents += '\n#include <main/nodemodels/' + modelName + 'Model.hpp>\n'
for param in parameterSet:
	contents += '#include <main/datatypes/' + param + 'Data.hpp>\n'

contents += '\n' + modelName + 'View::' + modelName + 'View(Flow::ParameterFactory& parameterFactory)\n'
contents += '	: Flow::NodeView(\n'
contents += '		Flow::Node::create<' + modelName + 'Model>(),\n'
contents += '		"{' + str(uuid.uuid4()) + '}",\n'
contents += '		parameterFactory)\n'
contents += '{\n'
for param in inputParameters:
	contents += '	' + param[1] + 'Parameter_ = std::move(parameterFactory.create' + param[2] + 'Parameter());\n'
contents += '\n'
for param in inputParameters:
	upperCaseName = param[1][0].upper() + param[1][1:]
	contents += '	QObject::connect(' + param[1] + 'Parameter_.get(), &Flow::NodeParameter::valueChanged, this, &' + modelName + 'View::update' + upperCaseName + 'Binding);\n'
contents += '\n'
for param in inputParameters:
	upperCaseName = param[1][0].upper() + param[1][1:]
	contents += '	update' + upperCaseName + 'Binding();\n'
contents += '}\n'
for param in inputParameters:
	contents += '\n'
	contents += 'Flow::' + param[0] + 'Parameter& ' + modelName + 'View::' + param[1] + 'Parameter()\n'
	contents += '{\n'
	contents += '	return *(' + param[1] + 'Parameter_.get());\n'
	contents += '}\n'

for param in inputParameters:
	contents += '\n'
	upperCaseName = param[1][0].upper() + param[1][1:]
	contents += 'void ' + modelName + 'View::update' + upperCaseName + 'Binding()\n'
	contents += '{\n'
	contents += '	nodeDataModel().bindInput(std::make_shared<' + param[0] + 'Data>(' + param[1] + 'Parameter_->getValue()), 0);\n'
	contents += '}\n'

contents += '\n'
contents += 'QJsonObject ' + modelName + 'View::saveModel() const\n'
contents += '{\n'
contents += '	QJsonObject modelJson;\n\n\n\n'
contents += '	return modelJson;\n'
contents += '}\n'

contents += '\n'
contents += 'void ' + modelName + 'View::restoreModel(QJsonObject const & p)\n'
contents += '{\n\n'
contents += '}\n'

contents += '\n\n\n\n'

contents += '// Qml' + modelName + 'View.hpp\n'
contents += '#pragma once\n'
contents += '\n'
contents += '#include <main/nodeviews/qml/QmlNodeView.hpp>\n'
contents += '#include <main/nodeviews/' + modelName + 'View.hpp>\n'
contents += '\n'
contents += 'class Qml' + modelName + 'View\n'
contents += '	: public ' + modelName + 'View\n'
contents += '	, public QmlNodeView\n'
contents += '{\n'
contents += 'public:\n'
contents += '	Qml' + modelName + 'View(Flow::ParameterFactory& parameterFactory);\n'
contents += '\n'
contents += '	std::unique_ptr<Flow::NodeView> clone() const override final;\n'
contents += '};\n'

contents += '\n\n\n\n'

contents += '// Qml' + modelName + 'View.cpp\n'
contents += '#include <main/nodeviews/qml/Qml' + modelName + 'View.hpp>\n'
contents += '\n'
for param in fullParameterSet:
	contents += '#include <main/parameters/Qml' + param + 'Parameter.hpp>\n'
contents += '\n'
contents += 'Qml' + modelName + 'View::Qml' + modelName + 'View(Flow::ParameterFactory& parameterFactory)\n'
contents += '	: ' + modelName + 'View(parameterFactory)\n'
contents += '	, QmlNodeView("' + modelUserName + '", ":/images/dummy.png")\n'
contents += '{\n'
for param in inputParameters:
	contents += '	addParameter(&(static_cast<Qml' + param[2] + 'Parameter&>(' + param[1] + 'Parameter())));\n'
contents += '}\n'
contents += '\n'
contents += 'std::unique_ptr<Flow::NodeView> Qml' + modelName + 'View::clone() const\n'
contents += '{\n'
contents += '	return std::make_unique<Qml' + modelName + 'View>(parameterFactory_);\n'
contents += '}\n'

write_contents(contents)