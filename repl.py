
import ako

if __name__ == "__main__":
  while True:
    incoming = input(">> ")
    prog = ako.parse(incoming)
    for stmt in prog: print(ako.eval(stmt))
