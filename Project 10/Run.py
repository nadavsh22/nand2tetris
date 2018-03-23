import CompilationEngine
import sys
import os
import Consts


def doAll(name):
    """
    runs the compiler for a specific ".jack" file, or, if given a directory
    name, runs the translator for all ".jack" files in directory
    :param name: file/directory name
    """
    if Consts.OLD_SUFFIX == name.split('.')[-1]:
        engine = CompilationEngine.CompilationEngine(name)
        engine.compileClass()
        engine.closeWriter()
    else:
        for fileName in os.listdir(name):
            if Consts.OLD_SUFFIX == fileName.split('.')[-1]:
                engine = CompilationEngine.CompilationEngine(name + "//" + fileName)
                engine.compileClass()
                engine.closeWriter()


if __name__ == "__main__":
    doAll(sys.argv[1])
