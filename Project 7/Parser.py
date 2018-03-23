############################################################
# Imports
############################################################

import VMConsts as Consts


############################################################
# Class definition
############################################################


class Parser:
    """
    A Parser object. Initiallized with a valid input file, and keeps all
    commands, and using public methods can output a first-level parsing of the
    command - command type, and one/two arguments.
    can
    """

    def __init__(self, filename):
        """
        Initializes the Parser object, reading all commands from filename.
        Initially the current command is empty. Should use advance to get the
        next command.
        """
        self.__commands = []
        self.__num_commands = 0
        self._init_commands(filename)

        self.__curr_cmd_idx = 0

        self.__commandType = None
        self.__arg1 = None
        self.__arg2 = None

    def _init_commands(self, fileName):
        """
        Initializes the Parser object's command arguments.
        Reads all the commands (divides by line), cleans them up,
        writes the non-empty and non-comment ones into a list, and counts them.
        :param fileName: the name of the input file to read.
        """
        file = open(fileName, 'r')
        commands = file.readlines()
        for line in commands:
            temp_line = line.strip("\n")  # remove newline
            temp_line = temp_line.split("//")[0]  # remove comments
            if temp_line == "":
                continue
            self.__commands.append(temp_line)
        self.__num_commands = len(self.__commands)
        return

    def _parseCurrCommand(self):
        """
        Parses the current command, based on the index of current command,
        divides it into relevant parts (split by whitespace) and sets the
        Parser's private arg1, arg2 and commandType into the relevant values
        commandType is a string, so is arg1; arg2 is an int
        """
        command = self.__commands[self.__curr_cmd_idx]
        command_parts = command.split(" ")
        if len(command_parts) == Consts.C_OPERAND and command_parts[0] in Consts.C_AR_LIST:
            self.__commandType = Consts.C_ARITHMETIC
            self.__arg1 = command_parts[0]  # arithmetic - keep command itself
            return
        elif len(command_parts) == Consts.C_CMPLX and command_parts[0] in Consts.C_P_LIST:
            self.__commandType = command_parts[0]
            self.__arg1 = command_parts[1]
            self.__arg2 = int(command_parts[2])
            return
        else:
            self.__commandType = Consts.C_UNK
            self.__arg1 = Consts.C_UNK_MSG
            return

    def hasMoreCommands(self):
        """
        returns the ship's current location.
        :return: tuple of current (x,y) coordinates.
        """
        return self.__curr_cmd_idx < self.__num_commands

    def advance(self):
        """
        returns the ship's current location.
        :return: tuple of current (x,y) coordinates.
        """
        self._parseCurrCommand()
        self.__curr_cmd_idx += 1
        return

    def arg1(self):
        """"
        returns the first argument of the current command (string)
        """
        return self.__arg1

    def arg2(self):
        """"
        returns the second argument of the current command (int)
        """
        return self.__arg2

    def commandType(self):
        """"
        returns the command type of the current command (CONSTANT)
        """
        return self.__commandType
