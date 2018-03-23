import Parser
import CodeWriter
import VMConsts
import os
import sys


def parseFile(name, codeWriter):
    """
    receives file name and creates a ".asm" output file with same name,
    which is a translation from VM language to hack assembly language
    :param name: the name of the file
    """
    parser = Parser.Parser(name)
    while parser.hasMoreCommands():
        parser.advance()
        command_type = parser.commandType()
        if command_type == VMConsts.C_ARITHMETIC:
            codeWriter.writeArithmetic(parser.arg1())
        elif command_type == VMConsts.C_POP or command_type == VMConsts.C_PUSH:
            codeWriter.writePushPop(command_type, parser.arg1(),
                                    parser.arg2())
        elif command_type == "label":
            codeWriter.writeLabel(parser.arg1())
        elif command_type == "goto":
            codeWriter.writeGoto(parser.arg1())
        elif command_type == "if-goto":
            codeWriter.writeIf(parser.arg1())
        elif command_type == "return":
            codeWriter.writeReturn()
        elif command_type == "call":
            codeWriter.writeCall(parser.arg1(), parser.arg2())
        elif command_type == "function":
            codeWriter.writeFunction(parser.arg1(), parser.arg2())


def doAll(name):
    """
    runs the translator for a specific ".vm" file, or, if given a directory
    name, runs the translator for all ".vm" files in directory
    :param name: file/directory name
    """
    if ".vm" in name:
        outputName = name.strip(VMConsts.SOURCE_SUFFIX) + VMConsts.OUT_SUFFIX
        codeWriter = CodeWriter.CodeWriter(outputName)
        codeWriter.writeInit()
        parseFile(name, codeWriter)
    else:
        outputName = name.split("/")[-1]
        outputName = name + "//" + outputName + VMConsts.OUT_SUFFIX
        codeWriter = CodeWriter.CodeWriter(outputName)
        codeWriter.writeInit()
        for fileName in os.listdir(name):
            if ".vm" in fileName:
                codeWriter.setCurrentFile(fileName.strip(".vm"))
                parseFile(name + "//" + fileName, codeWriter)
        codeWriter.close()


if __name__ == "__main__":
    doAll(sys.argv[1])
