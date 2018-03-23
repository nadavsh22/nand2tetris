############################################################
# Imports
############################################################

import VMConsts as Consts


############################################################
# Class definition
############################################################

class CodeWriter:
    """
    an object responsible of translating a command in VM language to the
    hack assembly language, and writing it to a new '.asm' file.
    """
    __writer = None
    __conCounter = 0
    __fileName = None
    __callCounter = 0
    __shortFileName = None
    __currentFileName = None

    # declaration and return

    def __init__(self, outputName):
        """
        initialize a CodeWriter with an output file name
        :param outputName: string of file name
        """
        self.__fileName = outputName
        self.__writer = open(self.__fileName, 'w')
        self.__shortFileName = self.__fileName.split("//")[-1]
        self.__shortFileName = self.__shortFileName.split(".")[0]
        self.__currentFileName = self.__shortFileName

    def setCurrentFile(self, fileName):
        self.__currentFileName = fileName

    def __compVal(self, string):
        return {
            "eq": "JEQ",
            "gt": "JGT",
            "lt": "JLT",
            "sub": "-",
            "add": "+",
            "and": "&",
            "or": "|",
            "neg": "-",
            "not": "!"
        }[string]

    def close(self):
        """
        close the writer file object of the code writer
        """
        if self.__writer is not None:
            self.__writer.close()

    def writeArithmetic(self, VMInstruction):
        """
        translates an arithmetic command and writes it into the output file in
        hack assembly language
        :param VMInstruction:
        """
        self.__writeLine("// " + str(VMInstruction))
        if VMInstruction in ["or", "and", "add", "sub"]:
            self.__addOrAndSub(VMInstruction)
        elif VMInstruction in ["neg", "not"]:
            self.__neg_not(VMInstruction)
        else:
            self.__compare(VMInstruction)

    def __addOrAndSub(self, VMInstruction):
        """
        writes the stack add/or/and/sub (+,|,&,-) instructions in hack assembly
        to output file
        """
        self.__writeLine("@SP")
        self.__writeLine("M=M-1")
        self.__writeLine("A=M")
        self.__writeLine("D=M")
        self.__writeLine("@SP")
        self.__writeLine("A=M-1")
        self.__writeLine("M=M" + str(self.__compVal(VMInstruction)) + \
                         "D")

    def __neg_not(self, VMInstruction):
        """
        writes the stack neg/not (-/!) instructions in hack assembly to output
        file
        """
        self.__writeLine("@SP")
        self.__writeLine("A=M-1")
        self.__writeLine("M=" + str(self.__compVal(VMInstruction)) + "M")

    def __compare(self, VMInstruction):
        """
        writes the stack equal instructions in hack assembly to output
        file
        """
        self.__writeLine("@CHECK" + str(self.__conCounter))
        self.__writeLine("0;JMP")
        # do this in case (TRUE)
        self.__writeLine("(TRUE" + str(self.__conCounter) + ")")
        self.__writeLine("@SP")
        self.__writeLine("A=M-1")
        self.__writeLine("M=-1")
        self.__writeLine("@END" + str(self.__conCounter))
        self.__writeLine("0;JMP")
        # do this in case (FALSE)
        self.__writeLine("(FALSE" + str(self.__conCounter) + ")")
        self.__writeLine("@SP")
        self.__writeLine("A=M-1")
        self.__writeLine("M=0")
        self.__writeLine("@END" + str(self.__conCounter))
        self.__writeLine("0;JMP")
        # checking the case (CHECK)
        self.__writeLine("(CHECK" + str(self.__conCounter) + ")")
        self.__writeLine("@SP")
        self.__writeLine("M=M-1")
        self.__writeLine("A=M")
        self.__writeLine("D=M")  # get the last value
        self.__writeLine("@SP")
        self.__writeLine("A=M-1")
        self.__writeLine("D=M-D")  # get the value before the last
        self.__writeLine("@TRUE" + str(self.__conCounter))
        # write the appropriate jump condition
        self.__writeLine("D;" + str(self.__compVal(VMInstruction)))
        ########################################################
        self.__writeLine("@FALSE" + str(self.__conCounter))
        self.__writeLine("0;JMP")
        self.__writeLine("(END" + str(self.__conCounter) + ")")
        self.__conCounter += 1

    def __push(self, arg1, arg2):
        """
        writes the stack "push" instructions in hack assembly to output
        file
        """
        self.__writeLine("@" + str(arg2))
        self.__writeLine("D=A")  # D = arg2
        if arg1 != "constant":
            self.__writeLine("@" + str(self.__segVal(arg1)))
            self.__writeLine("A=D+M")  # A = arg2 + base address
            self.__writeLine("D=M")
        self.__writeLine("@SP")
        self.__writeLine("A=M")
        self.__writeLine("M=D")
        self.__writeLine("@SP")
        self.__writeLine("M=M+1")

    def __pushTemp(self, arg2):
        """
        writes the stack "push" instructions in hack assembly to output
        file, specific for the temp segment (which is located at SEG_TEMP
        """
        self.__writeLine("@" + str(arg2 + Consts.SEG_TEMP))
        self.__writeLine("D=M")
        self.__writeLine("@SP")
        self.__writeLine("A=M")
        self.__writeLine("M=D")
        self.__writeLine("@SP")
        self.__writeLine("M=M+1")

    def __popTemp(self, arg2):
        """
        writes the stack "pop" to temp segment instruction in hack
        assembly code to output file
        :param arg2: the index within the segment to write to
        """

        self.__writeLine("@SP")
        self.__writeLine("M=M-1")
        self.__writeLine("A=M")
        self.__writeLine("D=M")
        self.__writeLine("@" + str(arg2 + Consts.SEG_TEMP))
        self.__writeLine("M=D")

    def __pushPointer(self, arg2):
        """
        writes the stack "push" from static segment instruction in hack
        assembly code to output file
        :param arg2: the index within the segment to read from
        """
        self.__writeLine("@" + str(self.__segVal(arg2)))
        self.__writeLine("D=M")
        self.__writeLine("@SP")
        self.__writeLine("A=M")
        self.__writeLine("M=D")
        self.__writeLine("@SP")
        self.__writeLine("M=M+1")

    def __popPointer(self, arg2):
        """
        writes the stack "pop" to pointer segment instruction in hack
        assembly
        code to output file
        :param arg2: the index within the segment to write to
        """
        self.__writeLine("@SP")
        self.__writeLine("M=M-1")
        self.__writeLine("A=M")
        self.__writeLine("D=M")

        self.__writeLine("@" + str(self.__segVal(arg2)))
        self.__writeLine("M=D")

    def __pushStatic(self, arg2):
        """
        writes the stack "push" from static segment instruction in hack
        assembly code to output file
        :param arg2: the index within the segment to read from
        """
        self.__writeLine("@" + self.__currentFileName + "." + str(arg2))
        self.__writeLine("D=M")
        self.__writeLine("@SP")
        self.__writeLine("A=M")
        self.__writeLine("M=D")
        self.__writeLine("@SP")
        self.__writeLine("M=M+1")

    def __popStatic(self, arg2):
        """
        writes the stack "pop" to static segment instruction in hack
        assembly code to output file
        :param arg2: the index within the segment to write to
        """
        self.__writeLine("@SP")
        self.__writeLine("M=M-1")
        self.__writeLine("A=M")
        self.__writeLine("D=M")
        self.__writeLine("@" + self.__currentFileName + "." + str(arg2))
        self.__writeLine("M=D")

    def __pop(self, arg1, arg2):
        """
        writes the stack "pop" instruction in hack assembly to te output file
        :param arg1: segment
        :param arg2: index
        """
        self.__writeLine("@" + str(arg2))
        self.__writeLine("D=A")
        self.__writeLine("@" + str(self.__segVal(arg1)))
        self.__writeLine("D=D+M")
        self.__writeLine("@13")  # temp location for address
        self.__writeLine("M=D")
        self.__writeLine("@SP")
        self.__writeLine("M=M-1")
        self.__writeLine("A=M")
        self.__writeLine("D=M")

        self.__writeLine("@13")  # temp location for address
        self.__writeLine("A=M")
        self.__writeLine("M=D")

    def __segVal(self, string):
        """
        dictionary for segment names and labels
        :param string: segment name
        :return: segment label
        """
        return {
            "local": "LCL",
            "argument": "ARG",
            "this": "THIS",
            "that": "THAT",
            "temp": Consts.SEG_TEMP,
            0: "THIS",
            1: "THAT"
        }[string]

    def writePushPop(self, command, segment, index):
        self.__writeLine(
            "// " + str(command) + " " + str(segment) + " " + str(index) +
            "")
        if command == Consts.C_PUSH:
            if segment == "static":
                self.__pushStatic(index)
            elif segment == "pointer":
                self.__pushPointer(index)
            elif segment == "temp":
                self.__pushTemp(index)
            else:
                self.__push(segment, index)
        elif command == Consts.C_POP:
            if segment == "static":
                self.__popStatic(index)
            elif segment == "pointer":
                self.__popPointer(index)
            elif segment == "temp":
                self.__popTemp(index)
            else:
                self.__pop(segment, index)

    def writeInit(self):
        """
        writes the initialization commands in assembly to output file
        """
        self.__writeLine("//bootstrap code")
        self.__writeLine("@256")
        self.__writeLine("D=A")
        self.__writeLine("@SP")
        self.__writeLine("M=D")
        self.writeCall(Consts.INITIALIZE, 0)

    def writeLabel(self, label):
        """
        writes the label command in assembly
        :param label:
        :return:
        """
        self.__writeLine("(" + self.__shortFileName + "." + str(label) + ")")

    def writeGoto(self, label):
        self.__writeLine("// goto " + str(label))
        self.__writeLine("@" + self.__shortFileName + "." + str(label))
        self.__writeLine("0;JMP")

    def writeIf(self, label):
        self.__writeLine("// if-goto " + str(label))
        self.__writeLine("@SP")
        self.__writeLine("M=M-1")
        self.__writeLine("A=M")
        self.__writeLine("D=M")
        self.__writeLine("@" + self.__shortFileName + "." + str(label))
        self.__writeLine("D;JNE")

    def writeReturn(self):
        """
        write the assembly code for a functions return statement
        """
        self.__writeLine("// return")
        self.__writeLine("@LCL")
        self.__writeLine("D=M")
        self.__writeLine("@endFrame")
        self.__writeLine("M=D")  # endframe = LCL

        self.__writeLine("@5")  # retAddr=*(endFrame-5)
        self.__writeLine("A=D-A")
        self.__writeLine("D=M")
        self.__writeLine("@retAddr")
        self.__writeLine("M=D")

        self.__writeLine("@SP")
        self.__writeLine("M=M-1")
        self.__writeLine("A=M")
        self.__writeLine("D=M")  # D = RAM[SP] (return value)
        self.__writeLine("@ARG")
        self.__writeLine("A=M")
        self.__writeLine("M=D")  # *ARG=pop()
        self.__writeLine("@ARG")
        self.__writeLine("D=M+1")  # D = ARG+1 (address)
        self.__writeLine("@SP")
        self.__writeLine("M=D")  # SP=ARG+1
        self.__assignmentHelper("THAT", "endFrame", 1)
        self.__assignmentHelper("THIS", "endFrame", 2)
        self.__assignmentHelper("ARG", "endFrame", 3)
        self.__assignmentHelper("LCL", "endFrame", 4)
        self.__writeLine("@" + "retAddr")
        self.__writeLine("A=M")
        self.__writeLine("0;JMP")  # goto retAddr


    def __writeLine(self, string):
        """
        writes a single line to output file, with newline at the end
        :param string: 
        """
        self.__writer.write(str(string) + "\n")

    def __assignmentHelper(self, leftHand, rightHand, i):
        """
        assignment operator translation, i.e: THAT=*(endFrame-1)
        :param leftHand: label
        :param rightHand: segment\label
        :param i: index
        """
        self.__writeLine("@" + rightHand)
        self.__writeLine("D=M")
        self.__writeLine("@" + str(i))
        self.__writeLine("A=D-A")
        self.__writeLine("D=M")
        self.__writeLine("@" + leftHand)
        self.__writeLine("M=D")

    def writeCall(self, funcName, nArgs):
        """
        write call command in assembly
        :param funcName: function to be called
        :param nArgs: number of arguments te receives
        """
        self.__writeLine("// call " + funcName + " " + str(nArgs))
        retAddress = "retAddress" + str(self.__callCounter)

        self.__writeLine("@" + retAddress)
        self.__writeLine("D=A")
        self.__writeLine("@SP")
        self.__writeLine("M=M+1")
        self.__writeLine("A=M-1")
        self.__writeLine("M=D")  # push returnAddress

        self.__pushToStack("LCL")  # push before-func LCL
        self.__pushToStack("ARG")  # push before-func ARG
        self.__pushToStack("THIS")  # push before-func THIS
        self.__pushToStack("THAT")  # push before-func THAT
        self.__writeLine("@5")  # lets jump 5 places from args
        self.__writeLine("D=A")  # D = 5
        self.__writeLine("@" + str(nArgs))
        self.__writeLine("D=D+A")  # D = 5 + number of arguments
        self.__writeLine("@SP")
        self.__writeLine("D=M-D")  # D = SP - (5+ number of args)
        self.__writeLine("@ARG")
        self.__writeLine("M=D")  # ARG=SP-5-nArgs
        self.__writeLine("@SP")
        self.__writeLine("D=M")  # D = SP
        self.__writeLine("@LCL")
        self.__writeLine("M=D")  # LCL=SP
        self.writeGoto(funcName)  # goto funcName
        self.__writeLine("(" + retAddress + ")")
        self.__callCounter += 1

    def __pushToStack(self, label):
        """

        :param label:
        :return:
        """
        self.__writeLine("@" + label)
        self.__writeLine("D=M")
        self.__writeLine("@SP")
        self.__writeLine("M=M+1")
        self.__writeLine("A=M-1")
        self.__writeLine("M=D")  # push the address pointed by label

    def writeFunction(self, funcName, numVars):
        self.__writeLine(
            "// function" + " " + str(funcName) + " " + str(numVars))
        self.__writeLine("(" + self.__shortFileName + "." + funcName + ")")
        for i in range(numVars):
            self.writePushPop("push", "constant", 0)
