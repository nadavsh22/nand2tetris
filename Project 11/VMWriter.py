############################################################
# Imports
############################################################

import JackTokenizer
import Consts as co

CONST = 1
ARG = 2
LOCAL = 3
STATIC = 4
THIS = 5
THAT = 6
POINTER = 7
TEMP = 8

ADD = 1
SUB = 2
NEG = 3
EQ = 4
GT = 5
LT = 6
AND = 7
OR = 8
NOT = 9
DIVIDE = "call Math.divide 2"
MULT = "call Math.multiply 2"


############################################################
# Class definition
############################################################
class VMWriter:
    """
    writes VMs. like, duh-doi
    """

    # segments = {CONST: "constant", ARG: "argument", LOCAL: "local",
    #             STATIC: "static", THIS: "this", THAT: "that", POINTER: "pointer",
    #             TEMP: "temp"}
    arithemetics = {"+": "add", '-': "sub", NEG: "neg", '=': "eq", '>': "gt",
                    '<': "lt", '&': "and", '|': "or", '~': "not", '*': MULT, '/': DIVIDE}

    def __init__(self, filename):
        """
        constructor, creates a new VM writer.
        Creates a new file and prepares it for writing VM commands.
        :param filename: the input file name
        """
        # self._tokenizer = JackTokenizer.JackTokenizer(filename)
        self._filename = filename
        self._writer = open(self._filename, 'w')

    def __writeLine(self, string):
        """
        writes a single line to output file, with newline at the end
        :param string: the string to write
        :return: None
        """
        self._writer.write(str(string) + "\n")

    def writePush(self, segment, Index):
        """
        Writes a VM 'push' command.
        :param segment: CONST, ARG, LOCAL, STATIC, THIS, THAT, POINTER or TEMP
        :param Index: integer
        :return: none
        """
        write = segment
        if segment == 'field':
            write = 'this'
        self.__writeLine("push " + write + " " + str(Index))

    def writePop(self, segment, Index):
        """
        Writes a VM 'pop' command.
        :param Segment: CONST, ARG, LOCAL, STATIC, THIS, THAT, POINTER or TEMP
        :param Index: integer
        :return: none
        """
        write = segment
        if segment == 'field':
            write = 'this'
        self.__writeLine("pop " + write + " " + str(Index))

    def writeArithmetic(self, command):
        """
        Writes a VM 'arithmetic' command.
        :param Segment: ADD, SUB, NEG, EQ, GT, LT, AND, OR, NOT
        :return: none
        """
        self.__writeLine(self.arithemetics[command])

    def writeLabel(self, label):
        """
        Writes a VM 'label' command.
        :param label: string
        :return: none
        """
        self.__writeLine("label " + str(label))

    def writeGoto(self, label):
        """
        Writes a VM 'goto' command.
        :param label: string
        :return: none
        """
        self.__writeLine("goto " + str(label))

    def writeIf(self, label):
        """
        Writes a VM 'If-goto' command.
        :param label: string
        :return: none
        """
        self.__writeLine("if-goto " + str(label))

    def writeCall(self, name, nArgs):
        """
        Writes a VM 'call' command.
        :param name: string
        :param nArgs: integer number of arguments
        :return: none
        """
        self.__writeLine("call " + str(name) + " " + str(nArgs))

    def writeFunction(self, name, nLocals):
        """
        Writes a VM 'function' command.
        :param name: string
        :param nLocals: integer, number of local variables
        :return: none
        """
        self.__writeLine("function " + str(name) + " " + str(nLocals))

    def writeReturn(self):
        """
        Writes a VM 'return' command.
        :return: none
        """
        self.__writeLine("return")

    def close(self):
        """
        Closes the output file
        :return: none
        """
        self._writer.close()
