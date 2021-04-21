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
                        self.next()
                        return const_node(int(value))



                elif self.current_token.tok_value == "(":
                        self.next() 
                        value = self.expr()

                        if self.current_token.tok_value != ")":
                                print(f"parse error! value = {self.current_token.tok_value}")
                                raise
                        
                        self.next() 
                        return value

                

        def term(self):
                value = self.factor()
                while (token := self.current_token.tok_value) in ("*", "/"):
                        self.next()
                        tmp = self.factor()
                        value = mul_node(left=value, right=tmp) if token == "*" else  div_node(left=value, right=tmp)
                        
                return value
                

        def expr(self):
                value = self.term()
                while (token := self.current_token.tok_value) in ("+", "-"):
                        self.next()
                        tmp = self.term()
                        value = add_node(left=value, right=tmp) if token == "+" else sub_node(left=value, right=tmp)

                return value




if __name__ == '__main__':
        ast_root = Interpreter("test_token").expr()
        result = ast_root.visit()
        print(result)





