from node import *
import tokenize
import sys


class Token:
        def __init__(self, tok_num, tok_value):
                self.tok_num = tok_num
                self.tok_value = tok_value

class Interpreter:
        def __init__(self, text_file):
                f = open(text_file, 'r')
                self.token_gen = tokenize.generate_tokens(f.readline)
                toknum, tokvalue, *_ = next(self.token_gen)
                self.current_token = Token(toknum, tokvalue)

        def next(self):
                toknum, tokvalue, *_ = next(self.token_gen)
                self.current_token = Token(toknum, tokvalue)

        def factor(self):
                if self.current_token.tok_num == tokenize.NUMBER:
                        value = self.current_token.tok_value


                elif self.current_token.tok_value == "(":
                        self.next() 
                        value = self.expr()

                        if self.current_token.tok_value != ")":
                                print(f"parse error! value = {self.current_token.tok_value}")
                                raise

                self.next()

                # print(f"Call Factor, return {value}")   
                return int(value)

        def term(self):
                value = self.factor()
                while (token := self.current_token.tok_value) in ("*", "/"):
                        self.next()
                        tmp = self.factor()
                        if token == "*": value *= tmp
                        else : value /= tmp

                # print(f"Call Term, return {value}")
                return value
                

        def expr(self):
                value = self.term()
                while (token := self.current_token.tok_value) in ("+", "-"):
                        self.next()
                        tmp = self.term()
                        if token == "+": value += tmp
                        else : value -= tmp
                
                # print(f"Call Expr, return {value}")
                return value




if __name__ == '__main__':
        result = Interpreter("test_token").expr()
        print(result)





