
import sys
import os

SYMBOL_LET = "("
AINST_LET = "@"
COMMENT_LET = "//"
SUFFIX = ".hack"

C_INST = 0
A_INST = 1
SYMB = 2
COMMENT = 3

FST_N = 16


def init_symbols():
    """
    Return a dictionary holding the default symbols of the assembler language
    """
    symb_dict = {"SP": "0", "LCL": "1", "ARG": "2", "THIS": "3", "THAT": "4",
                 "SCREEN": "16384", "KBD": "24576"}
    for i in range(FST_N):
        label = "R" + str(i)
        symb_dict[label] = i
    return symb_dict


def classify_inst(instruction):
    """
    Classify a code instruction
    :param instruction: a string representing a single code instruction
    :return: classification of the instruction - A/C instruction or a symbol
    """
    if instruction[0] == SYMBOL_LET:
        return SYMB
    if instruction[0] == AINST_LET:
        return A_INST
    if instruction[:2] == COMMENT_LET:
        return COMMENT
    return C_INST


def is_A_symb(instruction, symbols, curr_n):
    """
    Gets an A instruction and checks whether it's a symbol or not.
    if it is, checks whether it is a known symbol or not. If not, adds it
    to the dictionary of symbols.
    :param instruction: a string holding the A instruction
    :param symbols: current dictionary of symbols
    :param curr_n: current n integer (next memory cell to allocate)
    :return: the fixed instruction string, and the new n int
    """
    temp = instruction[1:]
    if not temp.isnumeric():  # true if it's not only numbers
        if temp not in symbols:
            symbols[temp] = curr_n
            curr_n += 1
    else:
        return instruction, curr_n
    retstr = instruction[0] + str(symbols[temp])
    return retstr, curr_n


def ATranslator(Ainstruction):
    """
    Parses a string representing an A instruction into its 16-bit repr.
    Assumes the Ainstruction is of format "@PositiveInteger"
    :param Ainstruction: a string representing an A instruction.
    :return: a string representing the binary representation of the instr.
    """
    # remove the @ and parse
    binstr = "{0:016b}".format(int(Ainstruction[1:]))  # format
    return binstr


def add_symb(instruction, symbols, curr_line):
    """
    Gets an instruction of the format "(xxx)" and the current symbols dict,
    and the current line number, and adds the symbol to the dictionary with
    the matching line number.
    """
    temp = instruction[1:-1]
    symbols[temp] = (curr_line)
    return


def destination(dest):
    d1 = d2 = d3 = "0"
    if 'M' in dest:
        d3 = "1"
    if 'D' in dest:
        d2 = "1"
    if 'A' in dest:
        d1 = "1"
    return d1 + d2 + d3


def jumpVal(string):
    return {
        "JGT": "001",
        "JEQ": "010",
        "JGE": "011",
        "JLT": "100",
        "JNE": "101",
        "JLE": "110",
        "JMP": "111"
    }[string]


def compVal(string):
    return {
        "0": "110101010",
        "1": "110111111",
        "-1": "110111010",
        "D": "110001100",
        "A": "110110000",
        "M": "111110000",
        "!D": "110001101",
        "!A": "110110001",
        "!M": "111110001",
        "-D": "110001111",
        "-A": "110110011",
        "-M": "111110011",
        "D+1": "110011111",
        "A+1": "110110111",
        "M+1": "111110111",
        "D-1": "110001110",
        "A-1": "110110010",
        "M-1": "111110010",
        "D+A": "110000010",
        "D+M": "111000010",
        "D-A": "110010011",
        "D-M": "111010011",
        "A-D": "110000111",
        "M-D": "111000111",
        "D&A": "110000000",
        "D&M": "111000000",
        "D|A": "110010101",
        "D|M": "111010101",
        "D<<": "010110000",
        "D>>": "010010000",
        "M>>": "011000000",
        "M<<": "011100000",
        "A>>": "010000000",
        "A<<": "010100000",

    }[string]


def c_trans(inst):
    """receives a string representing a c instruction and translating it to a
    16-bit binary command"""
    stringTop = "1"
    parts = inst.split('=')
    if len(parts) == 2:
        dest = destination(parts[0])
        restOfString = 1
    else:
        dest = destination("")
        restOfString = 0
    parts = parts[restOfString].split(';')
    if len(parts) == 2:
        jump = jumpVal(parts[1])
    else:
        jump = "000"
    comp = compVal(parts[0])
    return stringTop + comp + dest + jump


def parse_first_pass(line_string, symb_dict, line_num):
    """
    parses a line of assembly code for the first pass - checks if (xxx)
    """
    ins_class = classify_inst(line_string)
    keep = True
    if ins_class == SYMB:
        add_symb(line_string, symb_dict, line_num)
        keep = False
        return keep, line_num
    if ins_class == COMMENT:
        keep = False
        return keep, line_num
    return keep, (line_num + 1)


def parse_second_pass(line_string, symb_dict, open_memory):
    """
    parses a line of assembly code for the second pass - translates to binary
    """
    ins_class = classify_inst(line_string)
    if ins_class == A_INST:
        a_inst, open_memory = is_A_symb(line_string, symb_dict, open_memory)
        parsed = ATranslator(a_inst)
    elif ins_class == C_INST:
        parsed = c_trans(line_string)
    else:
        return "oh nooooo"
    return parsed, open_memory


def parseFile(fileName):
    """
    reads the filename and parses every line using two iterations
    :param fileName:
    :return:
    """
    writeFileName = fileName.split('.')[0]
    writeFileName = writeFileName + SUFFIX
    read = open(fileName, 'r')
    writeFile = open(writeFileName, "w")
    lines = list()
    i = 0
    symDict = init_symbols()
    for line in read:  # cleaning the file from unwanted comments/white spaces
        tempLine = line.strip("\n")  # remove newline
        tempLine = tempLine.strip("\r")  # remove newline
        tempLine = tempLine.split("//")[0]  # remove comments
        tempLine = tempLine.replace(" ", "")
        tempLine = tempLine.strip("\t")
        if tempLine == "":
            continue
        keep, i = parse_first_pass(tempLine, symDict, i)
        if keep:
            lines.append(tempLine)
    read.close()
    n = FST_N
    i = 0
    for line in lines:
        parsed, n = parse_second_pass(line, symDict, n)
        if i < len(lines) - 1:
            writeFile.write(parsed + "\n")
        else:
            writeFile.write(parsed)
        i += 1
    writeFile.close()


def doAll(name):
    if ".asm" in name:
        parseFile(name)
    else:
        for fileName in os.listdir(name):
            if ".asm" in fileName:
                parseFile(name + "//" + fileName)


if __name__ == "__main__":
    doAll(sys.argv[1])
