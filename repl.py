
from ako import parse
from ako import eval
from ako import Env
import ako

SHELL = Env([], [], None)

if __name__ == "__main__":
  while True:
    incoming = input(">> ")
    prog = parse(incoming)
    for stmt in prog:
        val = eval(stmt, ako.STD_ENV)
        if val != None: print(val)
