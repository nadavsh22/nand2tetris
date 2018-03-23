############################################################
# Imports
############################################################

import JackTokenizer
import Consts as co
import SymbolTable as st
import VMWriter as vm


############################################################
# Class definition
############################################################
# TO DO: arrays, tests, edge case
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
        self._className = filename.split('/')[-1].split('.')[0]
        self._filenameVM = filename.split('.')[0] + '.' + co.NEW_SUFFIX
        self._vmWriter = vm.VMWriter(self._filenameVM)
        self._simba = st.SymbolTable()
        self._ifCount = 0
        self._whileCount = 0

    ############################################################
    # Private methods
    ###########################################################

    def _compileElse(self):
        """
        compiles and writes the 'else' statement
        """
        # prints 'else'
        self._tokenizer.advance()
        # prints '{'
        self._tokenizer.advance()
        self.compileStatements()
        # prints '}'


    ############################################################
    # Public methods
    ###########################################################

    def compileClass(self):
        """
        compiles and writes the class
        """
        self._simba.startClass()
        self._tokenizer.advance()
        # prints 'Class
        self._tokenizer.advance()
        # prints class name
        self._tokenizer.advance()
        # prints '{'
        self._tokenizer.advance()

        while self._tokenizer.currentValue() != '}':

            if self._tokenizer.currentValue() in ['static', 'field']:

                self.compileClassVarDec()
                self._tokenizer.advance()
            elif self._tokenizer.currentValue() in ['constructor', 'function', 'method']:
                self.compileSubroutineDec()
                self._tokenizer.advance()

         # print }


    def compileVarDec(self):
        """
        compiles and writes the variable decleration
        :return:
        """
        kind = self._tokenizer.currentValue()  # save kind of variable
        self._tokenizer.advance()
        type = self._tokenizer.currentValue()  # save type of variable

        self._tokenizer.advance()
        while self._tokenizer.currentValue() != ';':
            if self._tokenizer.currentValue() != ",":  # if it's an identifier add it to symbol table
                name = self._tokenizer.currentValue()
                self._simba.define(name, type, kind)

            self._tokenizer.advance()

        # print ;


    def compileClassVarDec(self):
        """
        compiles and writes the class variable decleration
        :return:
        """

        kind = self._tokenizer.currentValue()  # save kind of variable

        self._tokenizer.advance()
        type = self._tokenizer.currentValue()  # save type of variable

        self._tokenizer.advance()
        while self._tokenizer.currentValue() != ';':
            if self._tokenizer.currentValue() != ",":  # if it's an identifier add it to symbol table
                name = self._tokenizer.currentValue()
                self._simba.define(name, type, kind)

            self._tokenizer.advance()


    def compileParameterList(self):
        """
        compiles and writes the parameter list
        :return:
        """
        kind = "argument"
        self._tokenizer.advance()
        i = 0
        while self._tokenizer.currentValue() != ')':
            if i % 3 == 0:
                type = self._tokenizer.currentValue()
            elif i % 3 == 1:
                varName = self._tokenizer.currentValue()
                self._simba.define(varName, type, kind)  # type is always defined before reaching this
                                                         # since the former if is reached in a previous iteration

            self._tokenizer.advance()
            i += 1


    def compileSubroutineDec(self):
        """
        compiles and writes the subroutine declaration
        :return:
        """
        self._simba.startSubroutine()

        subroutineType = self._tokenizer.currentValue()

        self._tokenizer.advance()
        returnType = self._tokenizer.currentValue()

        self._tokenizer.advance()
        functionName = self._tokenizer.currentValue()

        self._tokenizer.advance()

        # print (
        if subroutineType == 'method':  # methods use "this" as a first argument
            self._simba.define('this', self._className, 'argument')
        self.compileParameterList()
        # print )
        self.compileSubroutineBody(subroutineType, functionName)


    def compileSubroutineBody(self, subroutineType, functionName):
        """
        compiles and writes the subroutine declaration
        :return:
        """

        self._tokenizer.advance()
        # print {
        self._tokenizer.advance()

        while self._tokenizer.currentValue() == 'var':
            self.compileVarDec()
            self._tokenizer.advance()
        numVars = self._simba.varCount('local')
        self._vmWriter.writeFunction(self._className + '.' + functionName,
                                     numVars)  # print function declaration
        if subroutineType == 'method':
            self._vmWriter.writePush('argument', 0)
            self._vmWriter.writePop('pointer', 0)
        if subroutineType == 'constructor':
            numFields = self._simba.varCount('field')
            self._vmWriter.writePush('constant', numFields)
            self._vmWriter.writeCall("Memory.alloc", 1)
            self._vmWriter.writePop('pointer', 0)

        while self._tokenizer.currentValue() != '}':
            self.compileStatements()


    def compileStatements(self):
        """
        checks which is the current statement and compiles it
        """


        while self._tokenizer.currentValue() != '}':
            token = self._tokenizer.currentValue()
            if token == 'if':
                ifCount = self._ifCount
                self.compileIf(ifCount)
                self._tokenizer.advance()
                if self._tokenizer.currentValue() == 'else':
                    self._vmWriter.writeGoto("IF_END" + str(ifCount))
                    self._vmWriter.writeLabel("IF_FALSE" + str(ifCount))
                    self._compileElse()
                    self._vmWriter.writeLabel("IF_END" + str(ifCount))
                    self._tokenizer.advance()
                else:
                    self._vmWriter.writeLabel("IF_FALSE" + str(ifCount))
                    continue
            elif token == 'do':
                self.compileDo()
                self._tokenizer.advance()
            elif token == 'let':
                self.compileLet()
                self._tokenizer.advance()
            elif token == 'while':
                whileCount = self._whileCount
                self.compileWhile(whileCount)
                self._tokenizer.advance()
            elif token == 'return':
                self.compileReturn()
                self._tokenizer.advance()


    def compileDo(self):
        """
        compiles and writes the 'do' statement
        :return:
        """
        # prints do
        self._tokenizer.advance()
        firstToken = self._tokenizer.currentValue(), self._tokenizer.tokenType()
        self._tokenizer.advance()
        secondToken = self._tokenizer.currentValue(), self._tokenizer.tokenType()
        self.compileSubroutineCall(firstToken, secondToken)
        self._tokenizer.advance()
        # print the ';'
        self._vmWriter.writePop('temp', 0)  # write return value for void function/method

    def compileLet(self):
        """
        compiles and writes the 'let' statement
        """
        # prints 'let'
        self._tokenizer.advance()
        # prints 'varName'
        name = self._tokenizer.currentValue()
        segment = self._simba.kindOf(name)
        index = self._simba.indexOf(name)
        self._tokenizer.advance()
        assignToArray = False
        if self._tokenizer.currentValue() == '[':
            assignToArray = True
            # print '['
            self._tokenizer.advance()
            if not self._simba.isIn(name):
                print("the var " + name + " isn't in the symbol table")

            self.compileExpression('yes','left')
            self._vmWriter.writePush(self._simba.kindOf(name), self._simba.indexOf(name))
            self._vmWriter.writeArithmetic('+')
            # print ']'
            self._tokenizer.advance()
        # print '='
        self._tokenizer.advance()
        self.compileExpression('not', 'right')
        if not assignToArray:
            self._vmWriter.writePop(segment, index)
        # prints ';'
        if assignToArray:
            self._vmWriter.writePop('temp', 0)
            self._vmWriter.writePop('pointer', 1)
            self._vmWriter.writePush('temp', 0)
            self._vmWriter.writePop('that', 0)

    def compileWhile(self, whileCount):
        """
        compiles and writes the 'while' statement
        """
        self._vmWriter.writeLabel('WHILE_EXP' + str(whileCount))
        self._whileCount += 1
        # prints 'while'
        self._tokenizer.advance()
        # prints '('
        self._tokenizer.advance()
        self.compileExpression()
        self._vmWriter.writeArithmetic('~')
        self._vmWriter.writeIf("WHILE_END" + str(whileCount))
        # prints ')'
        self._tokenizer.advance()
        # prints '{'
        self._tokenizer.advance()
        self.compileStatements()
        self._vmWriter.writeGoto('WHILE_EXP' + str(whileCount))
        self._vmWriter.writeLabel("WHILE_END" + str(whileCount))
        # prints '}'

    def compileReturn(self):
        """
        compiles and writes the 'return' statement
        """
        # prints 'return'
        self._tokenizer.advance()
        if self._tokenizer.currentValue() != ';':
            self.compileExpression("not", "right")
        else:
            self._vmWriter.writePush('constant', 0)
        self._vmWriter.writeReturn()
        # prints ';'

    def compileIf(self, ifCount):
        """
        compiles and writes the 'if' statement
        """
        self._ifCount += 1
        # prints 'if'
        self._tokenizer.advance()
        # prints '('
        self._tokenizer.advance()
        self.compileExpression()
        self._vmWriter.writeIf('IF_TRUE' + str(ifCount))
        self._vmWriter.writeGoto('IF_FALSE' + str(ifCount))
        self._vmWriter.writeLabel('IF_TRUE' + str(ifCount))
        # prints ')'
        self._tokenizer.advance()
        # prints '{'
        self._tokenizer.advance()
        self.compileStatements()
        # prints '}'


    def compileExpression(self, arrayIndex ='not', leftRight ='right'):
        """
        VERY IMPORTANT NOTE: in order to look ahead in the term compiling,
        after calling compile expression, the current token is the one after the
        expression.
        :param arrayIndex: signifies whether current expression is index of an array or not.
        :param leftRight: signifies whether current expression is on the left side of an assignment or not
        (critical to handling of arrays)
        """
        self.compileTerm(arrayIndex, leftRight)
        currentToken = self._tokenizer.currentValue()
        i = 0
        while currentToken in ['+', '-', '*', '/', '&', '|', '<', '>', '=']:
            self._tokenizer.advance()
            self.compileTerm(arrayIndex, leftRight)
            self._vmWriter.writeArithmetic(currentToken)  # push op
            currentToken = self._tokenizer.currentValue()


    def compileTerm(self, arrayIndex = 'not', leftRight = 'left'):
        """
        VERY IMPORTANT NOTE: in order to look ahead in the term compiling,
        after calling compile expression, the current token is the one after the
        expression.
        :param arrayIndex: signifies whether current expression is index of an array or not.
        :param leftRight: signifies whether current expression is on the left side of an assignment or not
        (critical to handling of arrays)
        """

        firstToken = self._tokenizer.currentValue(), self._tokenizer.tokenType()
        self._tokenizer.advance()
        secondToken = self._tokenizer.currentValue(), self._tokenizer.tokenType()

        # integerConstant | stringConstant | keywordConstant
        if firstToken[1] in [co.STRING_CONST, co.INT_CONST] or firstToken[0] in [
            'true', 'false', 'this', 'null']:
            # print const
            if firstToken[1] == co.INT_CONST:
                self._vmWriter.writePush("constant", firstToken[0])
            elif firstToken[0] in ['true', 'false', 'null']:
                self._vmWriter.writePush("constant", 0)
                if firstToken[0] == 'true':
                    self._vmWriter.writeArithmetic('~')
            elif firstToken[0] == 'this':
                self._vmWriter.writePush('pointer', 0)
            elif firstToken[1] == co.STRING_CONST:
                string = firstToken[0]
                strLength = len(string)
                self._vmWriter.writePush('constant', strLength)
                self._vmWriter.writeCall('String.new', 1)
                for letter in string:
                    escaped = {8:'b', 9:'t', 10:'n', 11:'v', 12:'f',13:'r'}
                    ascii = ord(letter)
                    if ascii in escaped:  # escaped characters
                        self._vmWriter.writePush('constant', 116)  # 116 = \
                        self._vmWriter.writeCall('String.appendChar', 2)
                        self._vmWriter.writePush('constant', ord(escaped[ascii]))  # letter after \
                        self._vmWriter.writeCall('String.appendChar', 2)

                    else:
                        self._vmWriter.writePush('constant', ord(letter))
                        self._vmWriter.writeCall('String.appendChar', 2)

            return
        elif firstToken[0] in ['-', '~']:  # unaryOp term
            # print -/~
            self.compileTerm()
            if firstToken[0] == '-':
                write = vm.NEG
            else:
                write = firstToken[0]
            self._vmWriter.writeArithmetic(write)
            return

        elif firstToken[0] == '(':  # term = ('expression')
            # print '('
            self.compileExpression(arrayIndex, leftRight)  # everything within brackets
            # print ')'
            self._tokenizer.advance()

        elif secondToken[0] == '[':  # term = arrayname[expression]
            # prints varName
            # prints '['
            self._tokenizer.advance()
            self.compileExpression("yes", leftRight)
            index = self._simba.indexOf(firstToken[0])
            segment = self._simba.kindOf(firstToken[0])
            self._vmWriter.writePush(segment, index)
            self._vmWriter.writeArithmetic('+')

            if arrayIndex == 'yes':  # currently compiling something like array[secarray[4]]
                self._vmWriter.writePop('pointer', 1)
                self._vmWriter.writePush('that', 0)

            elif leftRight == 'right':
                self._vmWriter.writePop('pointer', 1)
                self._vmWriter.writePush('that', 0)
            # print ']'
            self._tokenizer.advance()

            # term = subroutineCall: subroutine(expressionList) | thing.subroutine(elist)
        elif firstToken[1] == co.IDENTIFIER and secondToken[0] in ['.', '(']:
            self.compileSubroutineCall(firstToken, secondToken)
            self._tokenizer.advance()

        else:  # a simple varName
            # prints varName
            name = firstToken[0]
            if not self._simba.isIn(name):
                print("the var " + name + " isn't in the symbol table")
            self._vmWriter.writePush(self._simba.kindOf(name), self._simba.indexOf(name))


    def compileSubroutineCall(self, firstToken, secondToken):
        """
        compiles and writes the a subroutine call
        """
        # prints varName|className|subroutineName
        objectName = firstToken[0]
        numExp = 0
        if secondToken[0] == '.':
            if self._simba.isIn(objectName):
                className = self._simba.typeOf(objectName)
                numExp += 1
                self._vmWriter.writePush(self._simba.kindOf(objectName),
                                         self._simba.indexOf(objectName))
            else:
                className = objectName  # object is a class object

            # prints  '.'
            self._tokenizer.advance()
            subName = self._tokenizer.currentValue()  # save subroutine Name
            subName = className + '.' + subName
            # print subroutineName
            self._tokenizer.advance()

        else:   #it's a method!!!
            numExp += 1
            subName = self._className + '.' + objectName
            self._vmWriter.writePush('pointer', 0)
        # print '('
        self._tokenizer.advance()

        numExp = numExp + self.compileExpressionList()
        self._vmWriter.writeCall(subName, numExp)
        # print ')'

    def compileExpressionList(self):
        """
        compiles and writes an expression list
        """

        if self._tokenizer.currentValue() == ')':
            return 0
        self.compileExpression("not", "right")
        expressionCount = 1
        while self._tokenizer.currentValue() == ',':
            # print ','
            self._tokenizer.advance()
            self.compileExpression("not","right")
            expressionCount += 1
        return expressionCount

    def closeWriter(self):
        self._vmWriter.close()
