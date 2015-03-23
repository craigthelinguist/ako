
import nakahi as nk

if __name__ == "__main__":
  while True:
    incoming = input(">> ")
    prog = nk.parse(incoming)
    print(nk.eval(prog))
