from stringUtils import *
import addFunctionWrappers

onlyExperimental = ["vr_camera"]

def generate(animationTypes, animationManagerFilePath):
    fileContents = """#include "KAnimationManagerFactory.h"
    
    #include "animation/KAnimationManager.h"
    
    """
    for animationType in animationTypes:
        capitalizedName = capitalize(animationType)
        fileContents += '#include "animation/types/' + animationType + '/K' + capitalizedName + 'ViewFactory.h"\n'
        fileContents += '#include "animation/types/' + animationType + '/K' + capitalizedName + 'NodeFactory.h"\n'
        fileContents += '#include "kscene/animation/types/' + animationType + '/K' + capitalizedName + 'AnimationType.h"\n'

    fileContents += """
    struct KAnimationManagerFactory::Private 
    {
      Private(QPointer<KUndoStack> undoStack) : """

    index = 0
    for animationType in animationTypes:
        capitalizedName = capitalize(animationType)
        camelCaseName = capitalizedName[0].lower() + capitalizedName[1:]
        fileContents += camelCaseName + 'ViewFactory(undoStack)'
        if index < len(animationTypes) - 1:
            fileContents += ', '
        index += 1

    fileContents += """{}
    
    """

    for animationType in animationTypes:
        capitalizedName = capitalize(animationType)
        camelCaseName = capitalizedName[0].lower() + capitalizedName[1:]
        fileContents += '  K' + capitalizedName + 'ViewFactory ' + camelCaseName + 'ViewFactory;\n'

    fileContents += """
      KAnimationManager animationManager;
    };
    
    // *************************************************************************************************
    KAnimationManagerFactory::KAnimationManagerFactory(luxScene_manager &sceneManager,
                                                   QPointer<KUndoStack> undoStack,
                                                   bool hasExperimentalFeatures)
    // *************************************************************************************************
    {
      d = std::make_unique<Private>(undoStack);
    """

    for animationType in animationTypes:
        capitalizedName = capitalize(animationType)
        camelCaseName = capitalizedName[0].lower() + capitalizedName[1:]
        if animationType in onlyExperimental:
            fileContents += '  if (hasExperimentalFeatures) {\n  '
        fileContents += '  d->animationManager.registerType(AnimationTypes::' + camelCaseName + ', &d->' + camelCaseName + 'ViewFactory,\nnew K' + capitalizedName + 'NodeFactory(sceneManager));\n'
        if animationType in onlyExperimental:
            fileContents += '  }'

    fileContents += """}
    
    // *************************************************************************************************
    KAnimationManagerFactory::~KAnimationManagerFactory()
    // *************************************************************************************************
    {
    }
    
    // *************************************************************************************************
    QPointer<KAnimationManager> KAnimationManagerFactory::getAnimationManager() const
    // *************************************************************************************************
    {
      return &d->animationManager;
    }
    """

    file = open(animationManagerFilePath, 'w')
    file.write(fileContents)
    file.close()

    addFunctionWrappers.add(animationManagerFilePath)
