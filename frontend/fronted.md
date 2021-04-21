## 一、編譯流程
由 python 內建的 disassembler 套件，可以看到函數的 Bytecode
```python
import dis
def foo():
        a = 2
        b = 3
        c = a + b

        for _ in range(c):
                yield _

if __name__ == "__main__":
        dis.dis(foo)
```
可以看到 bytecode 如下，接下來就由 python 虛擬機進行指令執行
```bash
  3           0 LOAD_CONST               1 (2)
              2 STORE_FAST               0 (a)

  4           4 LOAD_CONST               2 (3)
              6 STORE_FAST               1 (b)

  5           8 LOAD_FAST                0 (a)
             10 LOAD_FAST                1 (b)
             12 BINARY_ADD
             14 STORE_FAST               2 (c)

  7          16 LOAD_GLOBAL              0 (range)
             18 LOAD_FAST                2 (c)
             20 CALL_FUNCTION            1
             22 GET_ITER
        >>   24 FOR_ITER                10 (to 36)
             26 STORE_FAST               3 (_)

  8          28 LOAD_FAST                3 (_)
             30 YIELD_VALUE
             32 POP_TOP
             34 JUMP_ABSOLUTE           24
        >>   36 LOAD_CONST               0 (None)
             38 RETURN_VALUE
```

再來，Python 有個內建套件叫做 `tokenize`，幫助我們建立 `lexer(詞性分析器)`，十分便利
```python
import tokenize

if __name__ == "__main__":
        f = open("test_token", 'r')
        tk = tokenize.generate_tokens(f.readline)
        
        for item in tk:
                print(f"type: {item.type},   value: {item.string}")
```

做完詞性分析後，再來就是文法分析了。目的是將剛才標註的詞性建立起彼此連結，在此我們先以簡單的運算式為例子。
```
expr    = term   + term   + term   + ... + term
term    = factor * factor * factor * ... * factor
factor  = number | expr  
```
這裡實作兩種方式，一種是一般的 `parser`，一種轉成 `AST (抽象語法樹)`，轉成抽象語法樹方便我們之後生成 bytecode 的工作