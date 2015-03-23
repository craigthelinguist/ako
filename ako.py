

## Types.
## ------------------------------------------------------------

Symbol = str
List = list
Number = (int, float)



## Lexer/parser.
## ------------------------------------------------------------

def tokenise(program):
  return program.replace("(", " ( ").replace(")"," ) ").replace("'","' ").split()

def toatom(token):
  try:
    return int(token)
  except ValueError:
    try: return float(token)
    except ValueError: return Symbol(token)

def parse(program):
  program = tokenise(program)
  stack = []
  for token in program:
    if token == '(':
      stack.append(')')
    elif token == ')':
      l = []
      while stack[-1] != ')':
        l.append(stack.pop())
      stack.pop()
      l.reverse()
      stack.append(l)
    else:
      stack.append(toatom(token))
  return stack.pop()



## Standard Environment.
## ------------------------------------------------------------

STD_ENV = {}



## Interpreter.
## ------------------------------------------------------------

def eval(expr, env=STD_ENV):


  if type(expr) in Number:
    return expr

  fst = expr[0]

  if fst == "quote" or fst == "'":
    return expr[1]
  elif fst == "atom":
    return "t" if isinstance(expr[2], Symbol) else []
  elif fst == "eq":
    return expr[1] == expr[2]
  elif fst == "car":
    return expr[1][0]
  elif fst == "cdr":
    return expr[1][1:]
  elif fst == "cons":
    return [expr[1]] ++ expr[2]
  elif fst == "succ":
    return eval(expr[1]) + 1
  elif fst == "pred":
    return eval(expr[1]) - 1
  else:
    raise ValueError("Unknown token: " + str(expr[0]))


## Main.
## ------------------------------------------------------------
import sys

if __name__ == "__main__":
  fname = sys.argv[1]
  prog = None
  if fname.endswith(".ako"):
    with open(fname) as f: prog = f.read()
  if prog == None: sys.exit()
  prog = parse(prog)
  print(eval(prog))
