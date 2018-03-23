C_ARITHMETIC = 0
C_PUSH = "push"
C_POP = "pop"
C_RETURN = "return"

C_AR_LIST = ["add", "sub", "neg", "eq", "gt", "lt", "and", "or", "not"]
C_PFLOW_LIST = ["label", "goto", "if-goto"]
C_FUNC_LIST = ["function", "call"]
C_P_LIST = ["push", "pop"]
C_UNK_MSG = "UNKNOWN COMMAND"

C_OPERATOR = 1
C_CMPLX = 3
C_PFLOW = 2

SEG_LCL = 1
SEG_ARGUMENT = 2
SEG_CONSTANT = 3
SEG_STATIC = 4
SEG_TEMP = 5
SEG_POINTER = 6
SEG_THIS = 7
SEG_THAT = 8

INITIALIZE="Sys.init"

SOURCE_SUFFIX = ".vm"
OUT_SUFFIX = ".asm"
