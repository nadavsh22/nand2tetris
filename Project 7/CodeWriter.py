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

    def __init__(self, outputName):
        """
        initialize a CodeWriter with an output file name
        :param outputName: string of file name
        """
        self.__fileName = outputName
        self.__writer = open(self.__fileName, 'w')

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
        :return:
        """
        if self.__writer is not None:
            self.__writer.close()

    def writeArithmetic(self, VMInstruction):
        """
        translates an arithmetic command and writes it into the output file in
        hack assembly language
        :param VMInstruction:
        """
        self.__writer.write("// " + str(VMInstruction) + "\n")
        if VMInstruction in ["or", "and","add","sub"]:
            self.__addOrAndSub(VMInstruction)
        elif VMInstruction in ["neg","not"]:
            self.__neg_not(VMInstruction)
        else:
            self.__compare(VMInstruction)


    def __addOrAndSub(self, VMInstruction):
        """
        writes the stack add/or/and/sub (+,|,&,-) instructions in hack assembly
        to output file
        """
        self.__writer.write("@SP\n")
        self.__writer.write("M=M-1\n")
        self.__writer.write("A=M\n")
        self.__writer.write("D=M\n")
        self.__writer.write("@SP\n")
        self.__writer.write("A=M-1\n")
        self.__writer.write("M=M" + str(self.__compVal(VMInstruction)) + \
                            "D\n")

    def __neg_not(self, VMInstruction):
        """
        writes the stack neg/not (-/!) instructions in hack assembly to output
        file
        """
        self.__writer.write("@SP\n")
        self.__writer.write("A=M-1\n")
        self.__writer.write("M=" + str(self.__compVal(VMInstruction)) + "M\n")

    def __compare(self, VMInstruction):
        """
        writes the stack equal instructions in hack assembly to output
        file
        """
        self.__writer.write("@CHECK" + str(self.__conCounter) + "\n")
        self.__writer.write("0;JMP\n")
        # do this in case (TRUE)
        self.__writer.write("(TRUE" + str(self.__conCounter) + ")\n")
        self.__writer.write("@SP\n")
        self.__writer.write("A=M-1\n")
        self.__writer.write("M=-1\n")
        self.__writer.write("@END" + str(self.__conCounter) + "\n")
        self.__writer.write("0;JMP\n")
        # do this in case (FALSE)
        self.__writer.write("(FALSE" + str(self.__conCounter) + ")\n")
        self.__writer.write("@SP\n")
        self.__writer.write("A=M-1\n")
        self.__writer.write("M=0\n")
        self.__writer.write("@END" + str(self.__conCounter) + "\n")
        self.__writer.write("0;JMP\n")
        # checking the case (CHECK)
        self.__writer.write("(CHECK" + str(self.__conCounter) + ")\n")
        self.__writer.write("@SP\n")
        self.__writer.write("M=M-1\n")
        self.__writer.write("A=M\n")
        self.__writer.write("D=M\n") # get the last value
        self.__writer.write("@SP\n")
        self.__writer.write("A=M-1\n")
        self.__writer.write("D=M-D\n") # get the value before the last
        self.__writer.write("@TRUE" + str(self.__conCounter) + "\n")
        # write the appropriate jump condition
        self.__writer.write("D;" + str(self.__compVal(VMInstruction)) + "\n")
        ########################################################
        self.__writer.write("@FALSE" + str(self.__conCounter) + "\n")
        self.__writer.write("0;JMP\n")
        self.__writer.write("(END" + str(self.__conCounter) + ")\n")
        self.__conCounter += 1

    def __push(self, arg1, arg2):
        """
        writes the stack "push" instructions in hack assembly to output
        file
        """
        self.__writer.write("@" + str(arg2)+"\n")
        self.__writer.write("D=A\n")  # D = arg2
        if arg1 != "constant":
            self.__writer.write("@" + str(self.__segVal(arg1)) + "\n")
            self.__writer.write("A=D+M\n")  # A = arg2 + base address
            self.__writer.write("D=M\n")
        self.__writer.write("@SP\n")
        self.__writer.write("A=M\n")
        self.__writer.write("M=D\n")
        self.__writer.write("@SP\n")
        self.__writer.write("M=M+1\n")

    def __pushTemp(self, arg2):
        """
        writes the stack "push" instructions in hack assembly to output
        file, specific for the temp segment (which is located at SEG_TEMP
        """
        self.__writer.write("@" + str(arg2+Consts.SEG_TEMP)+"\n")
        self.__writer.write("D=M\n")
        self.__writer.write("@SP\n")
        self.__writer.write("A=M\n")
        self.__writer.write("M=D\n")
        self.__writer.write("@SP\n")
        self.__writer.write("M=M+1\n")

    def __popTemp(self, arg2):
        """
        writes the stack "pop" to temp segment instruction in hack
        assembly code to output file
        :param arg2: the index within the segment to write to
        """

        self.__writer.write("@SP\n")
        self.__writer.write("M=M-1\n")
        self.__writer.write("A=M\n")
        self.__writer.write("D=M\n")
        self.__writer.write("@" + str(arg2+Consts.SEG_TEMP) + "\n")
        self.__writer.write("M=D\n")

    def __pushPointer(self, arg2):
        """
        writes the stack "push" from static segment instruction in hack
        assembly code to output file
        :param arg2: the index within the segment to read from
        """
        self.__writer.write("@" + str(self.__segVal(arg2)) + "\n")
        self.__writer.write("D=M\n")
        self.__writer.write("@SP\n")
        self.__writer.write("A=M\n")
        self.__writer.write("M=D\n")
        self.__writer.write("@SP\n")
        self.__writer.write("M=M+1\n")

    def __popPointer(self, arg2):
        """
        writes the stack "pop" to pointer segment instruction in hack
        assembly
        code to output file
        :param arg2: the index within the segment to write to
        """
        self.__writer.write("@SP\n")
        self.__writer.write("M=M-1\n")
        self.__writer.write("A=M\n")
        self.__writer.write("D=M\n")

        self.__writer.write("@" + str(self.__segVal(arg2)) + "\n")
        self.__writer.write("M=D\n")

    def __pushStatic(self, filename, arg2):
        """
        writes the stack "push" from static segment instruction in hack
        assembly code to output file
        :param arg2: the index within the segment to read from
        """
        name = filename.split("//")[-1]
        name = name.split(".")[0]

        self.__writer.write("@" + name + "." + str(arg2) + "\n")
        self.__writer.write("D=M\n")
        self.__writer.write("@SP\n")
        self.__writer.write("A=M\n")
        self.__writer.write("M=D\n")
        self.__writer.write("@SP\n")
        self.__writer.write("M=M+1\n")

    def __popStatic(self, filename, arg2):
        """
        writes the stack "pop" to static segment instruction in hack
        assembly code to output file
        :param arg2: the index within the segment to write to
        """
        name = filename.split("//")[-1]
        name = name.split(".")[0]

        self.__writer.write("@SP\n")
        self.__writer.write("M=M-1\n")
        self.__writer.write("A=M\n")
        self.__writer.write("D=M\n")
        self.__writer.write("@" + name + "." + str(arg2) + "\n")
        self.__writer.write("M=D\n")

    def __pop(self, arg1, arg2):
        """
        writes the stack "pop" instruction in hack assembly to te output file
        :param arg1: segment
        :param arg2: index
        """
        self.__writer.write("@" + str(arg2) + "\n")
        self.__writer.write("D=A\n")
        self.__writer.write("@" + str(self.__segVal(arg1)) + "\n")
        self.__writer.write("D=D+M\n")
        self.__writer.write("@13\n")  # temp location for address
        self.__writer.write("M=D\n")
        self.__writer.write("@SP\n")
        self.__writer.write("M=M-1\n")
        self.__writer.write("A=M\n")
        self.__writer.write("D=M\n")

        self.__writer.write("@13\n")  # temp location for address
        self.__writer.write("A=M\n")
        self.__writer.write("M=D\n")

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
        self.__writer.write(
            "// " + str(command) + " " + str(segment) + " " + str(index) +
            "\n")
        if command == Consts.C_PUSH:
            if segment == "static":
                self.__pushStatic(self.__fileName, index)
            elif segment == "pointer":
                self.__pushPointer(index)
            elif segment == "temp":
                self.__pushTemp(index)
            else:
                self.__push(segment, index)
        elif command == Consts.C_POP:
            if segment == "static":
                self.__popStatic(self.__fileName, index)
            elif segment == "pointer":
                self.__popPointer(index)
            elif segment == "temp":
                self.__popTemp(index)
            else:
                self.__pop(segment, index)
