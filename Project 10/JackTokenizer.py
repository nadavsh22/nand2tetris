############################################################
# Imports
############################################################

import Consts as co
import re


############################################################
# Class definition
############################################################


class JackTokenizer:
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
        self._fileReader = open(filename, 'r')
        self._lines = self._fileReader.readlines()
        self._tokens = self._tokenizer(self._lines)
        self._currentTokenType = co.TOKEN_ERROR
        self._currentValue = ''

    ############################################################
    # private methods
    ############################################################
    def _identifyToken(self, word):
        """
        receives a string, tries matching to a recognised regex
        :param word: the string that is to be matched
        :return: the value of the given keyword, and the word
        """
        if re.match(co.KEYWORD_REGEX, word) or word in co.keywords:
            return co.KEYWORD, word.strip(" ")
        elif re.match(co.SYMBOLS_REGEX, word):
            return co.SYMBOL, word
        elif re.match(co.INT_CON_REGEX, word):
            return co.INT_CONST, word
        elif re.match(co.STR_CON_REGEX, word):
            return co.STRING_CONST, word[1:-1]
        elif re.match(co.IDENT_REGEX, word):
            return co.IDENTIFIER, word
        else:
            return co.TOKEN_ERROR, word

    def _findAllMatches(self, line):
        """
        find matches in lines and return a list all non-overlapping matches
        :param line: a list of lines
        :return: a list of matches
        """
        wordsInLine = co.LEXICAL_ELEMENTS_REGEX.findall(line)
        retWords = []
        for word in wordsInLine:
            for subWord in word:
                if subWord not in ['', '\t', '\n', ' ', '\r']:
                    retWords.append(subWord)
        return retWords

    def _removeComments(self, text):
        """
        removes all comments from given text
        :param text: line or lines of text
        :return: same text, no comments
        """
        line1 = ""
        for line in text:
            line1 = line1 + line
        text = line1

        def replacer(match):
            s = match.group(0)
            if s.startswith('/'):
                return " "  # note: a space and not an empty string
            else:
                return s

        pattern = re.compile(r'//.*?$|/\*.*?\*/|\'(?:\\.|[^\\\'])*\'|"(?:\\.|[^\\"])*"', re.DOTALL | re.MULTILINE)
        longline = re.sub(pattern, replacer, text)
        lines = longline.split("\n")
        return lines

    def _tokenizer(self, lines):
        """
        receives all code lines and returns a list of all words in code.
        :param lines: a list of lines
        :return: a list of words
        """
        tokenList = []
        lines = self._removeComments(lines)
        for linenum, line in enumerate(lines):
            # if linenum == 5:
            #     print("yesh")
            words = self._findAllMatches(line)
            for i, word in enumerate(words):
                maxi = len(words)
                value = self._identifyToken(word)[1]
                if value == 'return' and (i + 1 == maxi or words[i + 1] == ';'):
                    tokenList.append((co.KEYWORD, value))
                elif value in ['false', 'true', 'null'] and (i + 1 == maxi or words[i + 1] in [')', ';', ',']):
                    tokenList.append((co.KEYWORD, value))
                elif value in ['if', 'while'] and (i + 1 == maxi or words[i + 1] == '('):
                    tokenList.append((co.KEYWORD, value))
                elif value == 'else' and (i + 1 == maxi or words[i + 1] == '{'):
                    tokenList.append((co.KEYWORD, value))
                elif value == 'this' and (i + 1 == maxi or words[i + 1] in ['.', ';', ')']):
                    tokenList.append((co.KEYWORD, value))
                else:
                    tokenList.append(self._identifyToken(word))

        return tokenList

    ############################################################
    # public methods
    ############################################################
    def hasMoreTokens(self):
        """

        :return:  return true if there are more tokens in input,
        false otherwise
        """
        if len(self._tokens) == 0:
            return False
        else:
            return True

    def advance(self):
        """
        make current token the next token
        :return: error if there are no more tokens
        """
        if self.hasMoreTokens() == True:
            newToken = self._tokens.pop(0)
            self._currentTokenType = newToken[0]
            self._currentValue = newToken[1]
        else:
            return co.TOKEN_ERROR

    def tokenType(self):
        """
        :return: the type of the current token
        """
        return self._currentTokenType

    def currentValue(self):
        """
        :return: return current value
        """
        return self._currentValue
