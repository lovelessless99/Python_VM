import tokenize
import abc

ADD = 0
SUB = 1
MUL = 2
DIV = 3

class const_node:
        def __init__(self, value):
                self.value = value

        def visit(self, visitor):
                visitor.visit_const(self)

        def cal_visit(self, visitor):
                return visitor.visit_const(self)

class binary_node:
        def __init__(self, /, *, op=None, left=None, right=None):
                self.mapping_op = {
                        "+": ADD,
                        "-": SUB,
                        "*": MUL,
                        "/": DIV
                }
                self.op = self.mapping_op.get(op)
                self.left = left
                self.right = right

        def visit(self, visitor):
                visitor.visit_binary_op(self)

        def cal_visit(self, visitor):
                return visitor.visit_binary_op(self)

class Visitor(metaclass=abc.ABCMeta):

        @abc.abstractmethod
        def visit_const(self, const_node):
                raise NotImplementedError

        @abc.abstractmethod
        def visit_binary_op(self, binary_node):
                raise NotImplementedError




class PrintVisitor(Visitor):
        def __init__(self):
                self.map_code = {
                        ADD: "ADD",
                        SUB: "SUB",
                        MUL: "MUL",
                        DIV: "DIV"
                }

        def visit_const(self, const_node):
                print(f"LOAD_CONST {const_node.value}")

        def visit_binary_op(self, binary_node):
                binary_node.left.visit(self)
                binary_node.right.visit(self)
                print(self.map_code.get(binary_node.op))

class OPCodeVisitor(Visitor):
        
        def visit_const(self, const_node):
                pass
        def visit_binary_op(self, binary_node):
                pass

class CalculateVisitor(Visitor):

        def visit_const(self, const_node):
                return const_node.value

        def visit_binary_op(self, binary_node):
                l_value = binary_node.left.cal_visit(self)
                r_value = binary_node.right.cal_visit(self)

                result = 0
                if   binary_node.op == ADD: result = l_value + r_value
                elif binary_node.op == SUB: result = l_value - r_value
                elif binary_node.op == MUL: result = l_value * r_value
                elif binary_node.op == DIV: result = l_value / r_value
                return result


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
                        value = binary_node(op=token, left=value, right=tmp)
                        
                return value
                

        def expr(self):
                value = self.term()
                while (token := self.current_token.tok_value) in ("+", "-"):
                        self.next()
                        tmp = self.term()
                        value = binary_node(op=token, left=value, right=tmp)
                return value


if __name__ == '__main__':
        ast_root = Interpreter("test_token").expr()
        print_visitor = PrintVisitor()
        cal_visitor   = CalculateVisitor()
        

        ast_root.visit(print_visitor)
        
        result = ast_root.cal_visit(cal_visitor)
        print(result)
        
        