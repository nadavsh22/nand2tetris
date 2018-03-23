############################################################
# Imports
############################################################

import JackTokenizer
import Consts as co


############################################################
# Class definition
############################################################
class CompilationEngine:
    """
    words describing what this class does
    """

    def __init__(self, filename):
        """
        constructor, creates a new compilation engine with the given input
        :param filename: the input file name
        """
        self._tokenizer = JackTokenizer.JackTokenizer(filename)
        self._filename = filename.split('.')[0] + '.' + co.NEW_SUFFIX
        self._writer = open(self._filename, 'w')

    ############################################################
    # Private methods
    ###########################################################
    def _tagOpenClose(self, openCloseBool, type='token'):
        """
        writes xml tags
        :param openCloseBool:indicates if it's open or close
        :param type:
        :return:
        """
        start = '<' + openCloseBool * '/'
        end = '>' + openCloseBool * '\n'
        # if type not in co.elementDict.keys():
        #     print("hey")
        self._writer.write(start + co.elementDict[type] + end)

    def _printBlockDef(self):
        """
        prints an xml block for current token
        :return:
        """
        self._printBlock(self._tokenizer.tokenType(), self._tokenizer.currentValue())

    def _compileElse(self):
        """
        compiles and writes the 'else' statement
        """
        self._printBlockDef()  # prints 'else'
        self._tokenizer.advance()
        self._printBlockDef()  # prints '{'
        self._tokenizer.advance()
        self.compileStatements()
        self._printBlockDef()  # prints '}'

    def _printBlock(self, tokenType, tokenVal):
        """
        prints an xml block
        :param tokenType:
        :param tokenVal:
        :return:
        """
        self._tagOpenClose(0, tokenType)
        val = tokenVal
        if tokenVal in ['<', '>', '&']:
            val = co.symbDict[tokenVal]
        self._writer.write(" " + val + " ")
        self._tagOpenClose(1, tokenType)

    ############################################################
    # Public methods
    ###########################################################

    def compileClass(self):
        """
        compiles and writes the class
        """
        self._writer.write('<class>\n')
        self._tokenizer.advance()
        self._printBlockDef()  # prints 'Class
        self._tokenizer.advance()
        self._printBlockDef()  # prints class name
        self._tokenizer.advance()
        self._printBlockDef()  # prints '{'
        self._tokenizer.advance()

        while self._tokenizer.currentValue() != '}':
            # print("compile field or subroutine")
            started_subdecs = 0
            if self._tokenizer.currentValue() in ['static', 'field']:
                # if started_subdecs != 0:
                # print("shouldn't put var after subroutine declarations!")
                self.compileClassVarDec()
                self._tokenizer.advance()
            elif self._tokenizer.currentValue() in ['constructor', 'function', 'method']:
                self.compileSubroutineDec()
                self._tokenizer.advance()

        self._printBlockDef()  # prints }
        self._writer.write('</class>\n')

    def testTokenizer(self):
        while self._tokenizer.hasMoreTokens():
            self._tokenizer.advance()
            self._tagOpenClose(0, self._tokenizer.tokenType())
            self._writer.write(" " + self._tokenizer.currentValue() + " ")
            self._tagOpenClose(1, self._tokenizer.tokenType())

    def compileVarDec(self):
        """
        compiles and writes the variable decleration
        :return:
        """
        self._writer.write('<varDec>\n')
        while (self._tokenizer.currentValue() != ';'):
            self._printBlockDef()
            if self._tokenizer.currentValue() == 'arrayLength':
                pass
            self._tokenizer.advance()

        self._printBlockDef()  # print ;
        self._writer.write('</varDec>\n')

    def compileClassVarDec(self):
        """
        compiles and writes the class variable decleration
        :return:
        """
        self._writer.write('<classVarDec>\n')
        self._printBlockDef()
        while (self._tokenizer.currentValue() != ';'):
            self._tokenizer.advance()
            self._printBlockDef()
        self._writer.write('</classVarDec>\n')

    def compileParameterList(self):
        """
        compiles and writes the parameter list
        :return:
        """
        self._writer.write('<parameterList>\n')
        self._tokenizer.advance()
        i = 0
        while self._tokenizer.currentValue() != ')':
            self._printBlockDef()
            self._tokenizer.advance()
            i += 1
        # if i==0:
        # self._writer.write("\\n")
        self._writer.write('</parameterList>\n')

    def compileSubroutineDec(self):
        """
        compiles and writes the subroutine declaration
        :return:
        """
        self._writer.write('<subroutineDec>\n')
        while self._tokenizer.currentValue() != '(':
            self._printBlockDef()
            self._tokenizer.advance()
        self._printBlockDef()  # print (
        self.compileParameterList()
        self._printBlockDef()  # print )
        self.compileSubroutineBody()
        self._writer.write('</subroutineDec>\n')

    def compileSubroutineBody(self):
        """
        compiles and writes the subroutine declaration
        :return:
        """
        self._writer.write('<subroutineBody>\n')
        self._tokenizer.advance()
        self._printBlockDef()  # print {
        self._tokenizer.advance()
        while self._tokenizer.currentValue() == 'var':
            self.compileVarDec()
            self._tokenizer.advance()
        while self._tokenizer.currentValue() != '}':
            self.compileStatements()
            self._printBlockDef()
        self._writer.write('</subroutineBody>\n')

    def compileStatements(self):
        """
        checks which is the current statement and compiles it
        """
        self._writer.write('<statements>\n')

        while self._tokenizer.currentValue() != '}':
            token = self._tokenizer.currentValue()
            if (token == 'if'):
                self._writer.write('<ifStatement>\n')
                self.compileIf()
                self._tokenizer.advance()
                if self._tokenizer.currentValue() == 'else':
                    self._compileElse()
                    self._writer.write('</ifStatement>\n')
                    self._tokenizer.advance()
                else:
                    self._writer.write('</ifStatement>\n')
                    continue
            elif (token == 'do'):
                self._writer.write('<doStatement>\n')
                self.compileDo()
                self._writer.write('</doStatement>\n')
                self._tokenizer.advance()
            elif token == 'let':
                self._writer.write('<letStatement>\n')
                self.compileLet()
                self._writer.write('</letStatement>\n')
                self._tokenizer.advance()
            elif token == 'while':
                self._writer.write('<whileStatement>\n')
                self.compileWhile()
                self._writer.write('</whileStatement>\n')
                self._tokenizer.advance()
            elif token == 'return':
                self._writer.write('<returnStatement>\n')
                self.compileReturn()
                self._writer.write('</returnStatement>\n')
                self._tokenizer.advance()
            elif token == 'else':
                self._compileElse()
            # else:
            #     print("something not right")
            #     pass # used for debugging
        self._writer.write('</statements>\n')

    def compileDo(self):
        """
        compiles and writes the 'do' statement
        :return:
        """
        self._printBlockDef()  # prints do
        self._tokenizer.advance()
        firstToken = self._tokenizer.currentValue(), self._tokenizer.tokenType()
        self._tokenizer.advance()
        secondToken = self._tokenizer.currentValue(), self._tokenizer.tokenType()
        self.compileSubroutineCall(firstToken, secondToken)
        self._tokenizer.advance()
        self._printBlockDef()  # print the ';'

    def compileLet(self):
        """
        compiles and writes the 'let' statement
        """
        self._printBlockDef()  # prints 'let'
        self._tokenizer.advance()
        self._printBlockDef()  # prints 'varName'
        self._tokenizer.advance()
        if self._tokenizer.currentValue() == '[':
            self._printBlockDef()  # print '['
            self._tokenizer.advance()
            self.compileExpression()
            self._printBlockDef()  # print ']'
            self._tokenizer.advance()
        self._printBlockDef()  # print '='
        self._tokenizer.advance()
        self.compileExpression()
        self._printBlockDef()  # prints ';'

    def compileWhile(self):
        """
        compiles and writes the 'while' statement
        """
        self._printBlockDef()  # prints 'while'
        self._tokenizer.advance()
        self._printBlockDef()  # prints '('
        self._tokenizer.advance()
        self.compileExpression()
        self._printBlockDef()  # prints ')'
        self._tokenizer.advance()
        self._printBlockDef()  # prints '{'
        self._tokenizer.advance()
        self.compileStatements()
        self._printBlockDef()  # prints '}'

    def compileReturn(self):
        """
        compiles and writes the 'return' statement
        """
        self._printBlockDef()  # prints 'return'
        self._tokenizer.advance()
        if self._tokenizer.currentValue() != ';':
            self.compileExpression()
        self._printBlockDef()  # prints ';'

    def compileIf(self):
        """
        compiles and writes the 'if' statement
        """
        self._printBlockDef()  # prints 'if'
        self._tokenizer.advance()
        self._printBlockDef()  # prints '('
        self._tokenizer.advance()
        self.compileExpression()
        self._printBlockDef()  # prints ')'
        self._tokenizer.advance()
        self._printBlockDef()  # prints '{'
        self._tokenizer.advance()
        self.compileStatements()
        self._printBlockDef()  # prints '}'

    def compileExpression(self):
        """
        VERY IMPORTANT NOTE: in order to look ahead in the term compiling,
        after calling compile expression, the current token is the one after the
        expression.
        """
        self._writer.write('<expression>\n')
        self.compileTerm()
        currentToken = self._tokenizer.currentValue()
        i = 0
        while currentToken in ['+', '-', '*', '/', '&', '|', '<', '>', '=']:
            self._printBlockDef()
            self._tokenizer.advance()
            self.compileTerm()
            currentToken = self._tokenizer.currentValue()
        self._writer.write('</expression>\n')

    def compileTerm(self):
        """
        VERY IMPORTANT NOTE: in order to look ahead in the term compiling,
        after calling compile expression, the current token is the one after the
        expression.
        """
        self._writer.write('<term>\n')
        firstToken = self._tokenizer.currentValue(), self._tokenizer.tokenType()
        self._tokenizer.advance()
        secondToken = self._tokenizer.currentValue(), self._tokenizer.tokenType()

        # integerConstant | stringConstant | keywordConstant
        if firstToken[1] in [co.STRING_CONST, co.INT_CONST] or firstToken[0] in [
            'true', 'false', 'this', 'null']:
            self._printBlock(firstToken[1], firstToken[0])  # print const
            self._writer.write('</term>\n')
            return
        elif firstToken[0] in ['-', '~']:  # unaryOp term
            self._printBlock(firstToken[1], firstToken[0])  # print -/~
            self.compileTerm()
            self._writer.write('</term>\n')
            return

        if firstToken[0] == '(':  # term = ('expression')
            self._printBlock(firstToken[1], firstToken[0])  # print '('
            self.compileExpression()  # everything within brackets
            self._printBlockDef()  # print ')'
            self._tokenizer.advance()


        elif secondToken[0] == '[':  # term = arrayname[expression]
            self._printBlock(firstToken[1], firstToken[0])  # prints varName
            self._printBlockDef()  # prints '['
            self._tokenizer.advance()
            self.compileExpression()
            self._printBlockDef()  # print ']'
            self._tokenizer.advance()

            # term = subroutineCall: subroutine(expressionList) | thing.subroutine(elist)
        elif firstToken[1] == co.IDENTIFIER and secondToken[0] in ['.', '(']:
            self.compileSubroutineCall(firstToken, secondToken)
            self._tokenizer.advance()

        else:  # a simple varName
            self._printBlock(firstToken[1], firstToken[0])  # prints varName

        self._writer.write('</term>\n')

    def compileSubroutineCall(self, firstToken, secondToken):
        """
        compiles and writes the a subroutine call
        """
        self._printBlock(firstToken[1], firstToken[0])  # prints
        # varName|className|subroutineName
        if secondToken[0] == '.':
            self._printBlockDef()  # prints  '.'
            self._tokenizer.advance()
            self._printBlockDef()  # print subroutineName
            self._tokenizer.advance()
        self._printBlockDef()  # print '('
        self._tokenizer.advance()
        self.compileExpressionList()
        self._printBlockDef()  # print ')'

    def compileExpressionList(self):
        """
        compiles and writes an expression list
        """
        self._writer.write('<expressionList>\n')
        if self._tokenizer.currentValue() == ')':
            self._writer.write('</expressionList>\n')
            return
        self.compileExpression()
        while self._tokenizer.currentValue() == ',':
            self._printBlockDef()  # print ','
            self._tokenizer.advance()
            self.compileExpression()
        self._writer.write('</expressionList>\n')

    def closeWriter(self):
        self._writer.close()
