############################################################
# Imports
############################################################

import JackTokenizer
import Consts as co


############################################################
# Class definition
############################################################
class SymbolTable:
    """
    A symbol table. duh
    a symboles key is its name, values are a tuple (type,kind,count)
    """

    def __init__(self):
        """
        constructor, creates a new empty symbol table
        :param filename: the input file name
        """
        self.__classSD = dict()  # Class-Scope Symbol Dictionary
        self.__subSD = dict()  # Subroutine-Scope Symbol Dictionary
        self.fieldCount = 0
        self.staticCount = 0
        self.localCount = 0
        self.argCount = 0

    def startSubroutine(self):
        """
        Starts a new subroutine scope (i.e. erases all names in the previous
        subroutine's scope.)
        :return: NONE
        """
        self.__subSD.clear()
        self.localCount = 0
        self.argCount = 0

    def startClass(self):
        """
        Starts a new subroutine scope (i.e. erases all names in the previous
        subroutine's scope.)
        :return: NONE
        """
        self.startSubroutine()
        self.__classSD.clear()
        self.staticCount = 0
        self.fieldCount = 0

    def define(self, name, type, kind):
        """
        Defines a new identifier of a given name, type and kind and assigns it
        a running index. STATIC and FIELD identifiers have a class scope,
        while ARG and VAR identifiers have a subroutine scope.
        :param name: String
        :param type: string int, boolean, char, className
        :param kind: STATIC, FIELD, ARG or VAR
        :return: NONE
        """
        if kind in ["field", "static"]:
            if kind == "field":
                index = self.fieldCount
                self.fieldCount += 1
            else:
                index = self.staticCount
                self.staticCount += 1
            self.__classSD[name] = (type, kind, index)
        elif kind in ['argument', 'var']:
            if kind == 'argument':
                index = self.argCount
                self.argCount += 1
                self.__subSD[name] = (type, kind, index)
            else:
                index = self.localCount
                self.localCount += 1
                self.__subSD[name] = (type, "local", index)

        else:
            print("erreur")

    def varCount(self, kind):
        """
        Returns the number of variables of the given kind already defined in the
        current scope.
        :param kind: STATIC, FIELD, ARG or VAR
        :return: number of instances in table (int)
        """
        if kind == "field":
            return self.fieldCount
        elif kind == "static":
            return self.staticCount
        elif kind == "local":
            return self.localCount
        elif kind == "argument":
            return self.argCount

    def kindOf(self, name):
        """
        Returns the kind of the names identifier in the current scope.
        Returns NONE if the identifier is unknown in the current scope.
        :param name: string, identifier to be identified
        :return: STATIC, FIELD, ARG or VAR (/NONE)
        """
        if name in self.__subSD:
            return self.__subSD[name][1]
        elif name in self.__classSD:
            return self.__classSD[name][1]
        else:
            return None

    def typeOf(self, name):
        """
        Returns the type of the names identifier in the current scope.
        :param name: string, identifier to be identified else return None
        :return: string - type
        """
        if name in self.__subSD:
            return self.__subSD[name][0]
        elif name in self.__classSD:
            return self.__classSD[name][0]
        else:
            return None

    def indexOf(self, name):
        """
        Returns the index assigned to names identifier.
        :param name: string, identifier to be identified
        :return: index (int)
        """
        if name in self.__subSD:
            return self.__subSD[name][2]
        elif name in self.__classSD:
            return self.__classSD[name][2]
        else:
            return None

    def isIn(self, name):
        return name in self.__subSD or name in self.__classSD
