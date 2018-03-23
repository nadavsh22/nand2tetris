import Parser
import CodeWriter
import VMConsts
import os
import sys

def parseFile(name):
    """
    receives file name and creates a ".asm" output file with same name,
    which is a translation from VM language to hack assembly language
    :param name: the name of the file
    """
    parser = Parser.Parser(name)
    outputName = name.strip(VMConsts.SOURCE_SUFFIX) + VMConsts.OUT_SUFFIX
    codeWriter = CodeWriter.CodeWriter(outputName)
    while parser.hasMoreCommands():
        parser.advance()
        command_type = parser.commandType()
        if command_type == VMConsts.C_ARITHMETIC:
            codeWriter.writeArithmetic(parser.arg1())
        elif command_type == VMConsts.C_POP or command_type == VMConsts.C_PUSH:
            codeWriter.writePushPop(command_type, parser.arg1(),
                                    parser.arg2())
    codeWriter.close()


def doAll(name):
    """
    runs the translator for a specific ".vm" file, or, if given a directory
    name, runs the translator for all ".vm" files in directory
    :param name: file/directory name
    """
    if ".vm" in name:
        parseFile(name)
    else:
        for fileName in os.listdir(name):
            if ".vm" in fileName:
                parseFile(name + "//" + fileName)


if __name__ == "__main__":
    doAll(sys.argv[1])
