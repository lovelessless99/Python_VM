import abc


mapping_code = {
        'add_node'   : 'BINARY_ADD',
        'sub_node'   : 'BINARY_SUB',
        'mul_node'   : 'BINARY_MUL',
        'div_node'   : 'BINARY_DIV',
        'const_node' : 'LOAD_CONST'
}


class node(metaclass=abc.ABCMeta):
        def __init__(self, /, *, left=None, right=None):
                self.left  = left
                self.right = right

        
        @abc.abstractmethod
        def visit(self):
                raise NotImplementedError


class add_node(node):
        def __init__(self, /, *, left=None, right=None):
                super().__init__(left=left, right=right)
        
        def visit(self):
                l_value = self.left.visit()
                r_value = self.right.visit()
                self.value = l_value + r_value 
                
                name = self.__class__.__name__
                print(f"{mapping_code.get(name, 0)}")
                return self.value


class sub_node(node):
        def __init__(self, /, *, left=None, right=None):
                super().__init__(left=left, right=right)

        def visit(self):
                l_value = self.left.visit()
                r_value = self.right.visit()
                self.value = l_value - r_value 

                name = self.__class__.__name__
                print(f"{mapping_code.get(name, 0)}")
                return self.value


class mul_node(node):
        def __init__(self, /, *, left=None, right=None):
                super().__init__(left=left, right=right)

        def visit(self):
                l_value = self.left.visit()
                r_value = self.right.visit()
                self.value = l_value * r_value

                name = self.__class__.__name__
                print(f"{mapping_code.get(name, 0)}")
                return self.value

class div_node(node):
        def __init__(self, /, *, left=None, right=None):
                super().__init__(left=left, right=right)
        
        def visit(self):
                l_value = self.left.visit()
                r_value = self.right.visit()
                self.value = l_value / r_value 

                name = self.__class__.__name__
                print(f"{mapping_code.get(name, 0)}")
                return self.value

class const_node(node):
        def __init__(self, value, /, *, left=None, right=None):
                super().__init__(left=left, right=right)
                self.value = value
                
        def visit(self): 
                name = self.__class__.__name__
                print(f"{mapping_code.get(name, 0)} {self.value}")
                return self.value