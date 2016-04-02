#!/usr/bin/env python
# encoding: utf-8

STRING,FUNCTION,INTEGER,EOF,END ="STRING","FUNCTION","INTEGER","EOF","."

class Token(object):
    def __init__(self, type, value):
        self.type = type
        self.value = value

    def __str__(self):
        return 'Token({type}, {value})'.format(
            type=self.type,
            value=repr(self.value)
        )

    def __repr__(self):
        return self.__str__()

class Lexer(object):
    def __init__(self, text):
        self.text = text
        self.pos = 0
        if self.text[self.pos] != None:
            self.current_char = self.text[self.pos]
            if text[len(text)-1]!='.':
                self.missingend()


    def missingend(self):
        raise Exception('dot is missing')
    def error(self):
        raise Exception('Error parsing input')

    def advance(self):
        self.pos += 1
        if self.pos > len(self.text) - 1:
            self.current_char = None
        else:
            self.current_char = self.text[self.pos]



    def skip_whitespace(self):
        while self.current_char is not None and self.current_char.isspace():
            self.advance()

    def integer(self):
        result = ""
        while self.current_char is not None and self.current_char.isdigit():
            result += self.current_char
            self.advance()
        return int(result)

    def strings(self):
        result = ''
        while self.current_char is not None and self.current_char != "." and not self.current_char.isdigit():
            while self.current_char is not None and isinstance(self.current_char,basestring) and not self.current_char.isdigit() and not self.current_char == " " and not self.current_char == '.':
                result += self.current_char
                self.advance()
            self.advance()
            if self.current_char is not None and isinstance(self.current_char,basestring) and not self.current_char.isdigit() and not self.current_char == " " and not self.current_char == '.':
                result += " "
        return result

    def stringa(self):
        result =''
        self.advance()
        while self.current_char is not None:
            while self.current_char is not None and self.current_char != "'" and self.current_char != " ":
                result += str(self.current_char)
                self.advance()
            self.advance()
            result += " "
            if self.current_char != "'":
                break
        return result

    def worthornot(self):
        result=''
        for i in range(0,2):
            result += str(self.current_char)
            self.advance()
        return  result

    def get_next_token(self):
        while self.current_char is not None:
            if self.current_char.isspace():
                self.skip_whitespace()
                continue
            if self.current_char == "'":
                check=self.stringa()
                token = Token(STRING, check)
                return token

            if self.current_char == '.':
                token = Token(END , '.')
                return token

            if self.current_char == '=' or self.current_char == '!':
                check = self.worthornot()
                if check == '==':
                    token = Token(STRING,"==")
                elif check == '!=':
                    token = Token(STRING,"!=")
                else :
                    continue
                return token

            if self.current_char.isdigit() and not self.current_char == "'":
                token = Token(INTEGER, self.integer())
                return token

            if isinstance(self.current_char,basestring) and not self.current_char.isdigit() and not self.current_char == "'":
                check = self.strings()
                if check == "לכל":
                    token = Token(FUNCTION , "לכל")
                elif check == "אם":
                    token = Token(FUNCTION, "אם")
                else:
                    self.error()
                #else:
                #    token = Token(STRING , check)
                return token

            self.error()

        return Token(EOF, None)

class Interpreter(object):
    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = self.lexer.get_next_token()

    def error(self):
        raise Exception('Invalid syntax')

    def eat(self, token_type):
        if self.current_token.type == token_type:
            self.current_token = self.lexer.get_next_token()
        else:
            self.error()

    def fors(self):
        if self.current_token.type is INTEGER:
            times = self.current_token.value
            return int(times)
        else:
            self.error()
            pass


    def Factor(self):
        token = self.current_token
        codes = ""
        if token.type is FUNCTION:
            if token.value == "לכל":
                self.eat(FUNCTION)
                times = self.fors()
                a=self.lexer.get_next_token()
                if a.value is not None:
                    if a.type is STRING and str(a.value) != "==" and str(a.value) != "!=":
                        codes += "'"
                        codes += str(a.value)
                        codes += "'"
                        codes += " "
                    else:
                        codes += str(a.value)
                        codes += " "
                while self.lexer.get_next_token().value is not None and str(self.current_token.value) is not '.' and (self.current_token.type is STRING or self.current_token.type is INTEGER or self.current_token.type is FUNCTION):
                    a= self.lexer.get_next_token()
                    if a.value == ".":
                        break
                    if a.type is STRING and str(a.value) != "==" and str(a.value) != "!=":
                        codes += "'"
                        codes += str(a.value)
                        codes += "'"
                        codes += " "
                    else:
                        codes += str(a.value)
                        codes += " "
                i = 0
                codes += '.'

                while i < times:
                    lexer = Lexer(codes)
                    interpreter = Interpreter(lexer)
                    result = interpreter.expr()
                    i += 1
            if token.value == "אם":
                self.eat(FUNCTION)
                condition=str(self.current_token.value)
                worthornot=str(self.lexer.get_next_token().value)
                condition2=str(self.lexer.get_next_token().value)
                while self.current_token.value is not None and str(self.current_token.value) is not '.' and (self.current_token.type is STRING or self.current_token.type is INTEGER or self.current_token.type is FUNCTION):
                    a= self.lexer.get_next_token()
                    if a.value == ".":
                        break
                    if a.type is STRING:
                        codes += "'"
                        codes += str(a.value)
                        codes += "'"
                        codes += " "
                    else:
                        codes += str(a.value)
                        codes += " "
                codes += '.'
                if worthornot == "==":
                    if condition == condition2:
                        lexer = Lexer(codes)
                        interpreter = Interpreter(lexer)
                        result = interpreter.expr()
                if worthornot == "!=":
                    if condition != condition2:
                        lexer = Lexer(codes)
                        interpreter = Interpreter(lexer)
                        result = interpreter.expr()

        if token.type is INTEGER:
            self.eat(INTEGER)
            return token.value

        if token.type is STRING:
            self.eat(STRING)
            print token.value
            return token.value

    def expr(self):
        return self.Factor()

def main():
    while True:
        try:
            text = raw_input()
        except EOFError:
            break
        if text == None:
            continue
        lexer = Lexer(text)
        interpreter = Interpreter(lexer)
        result = interpreter.expr()

if __name__ == '__main__':
    main()