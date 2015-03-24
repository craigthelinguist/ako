

## Types.
## ------------------------------------------------------------

Symbol = str
List = list
Number = (int, float)

class Env(dict):

    def __init__(self, args, vals, parent):
        for arg,val in zip(args,vals):
            self[arg] = val
        self.parent = parent

    def valueOf(self, var):
        if var in self: return self[var]
        if self.parent == None: raise ValueError("Unknown variable: " + var)
        return self.parent.valueOf(var)

class Func(object):

    def __init__(self, args, body, env):
        self.args = args
        self.body = body
        self.env = env

    def invoke(self, *args):
        return eval(self.body, Env(self.args, args, self.env))


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
  stack.append(')')
  program.append(')')
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

STD_ENV = Env([], [], None)

## Interpreter.
## ------------------------------------------------------------

def eval(expr, env=STD_ENV):

  # evaluate literals
  if type(expr) in Number:
    return expr
  elif isinstance(expr, Symbol):
    return env.valueOf(expr)

  # otherwise check what the expression is.
  fst = expr[0]

  # return the literal expression.
  if fst == "quote" or fst == "'": return expr[1]

  # return true if it is a symbol.
  elif fst == "atom":
    return "t" if isinstance(expr[2], Symbol) else []

  # test equality of two expressions
  elif fst == "eq":
      return expr[1] == expr[2]

  # car returns the head of a list.
  elif fst == "car":
      return expr[1][0]

  # return everything except the head of a list
  elif fst == "cdr":
      return expr[1][1:]

  # prepend element to list
  elif fst == "cons":
      return [expr[1]] ++ expr[2]

  # successor of the expression
  elif fst == "succ":
      return eval(expr[1]) + 1

  # predecessor of the expression
  elif fst == "pred":
      return eval(expr[1]) - 1

  # variable binding
  elif fst == "def":
      name, body = expr[1], expr[2]
      env[name] = body

  # lambda is for defining function literals
  elif fst == "lambda":
      return Func(expr[1], expr[2], env)

  # function invocation
  else:
    fn = eval(expr[0], env)
    argvs = [eval(arg, env) for arg in expr[1:]]
    Func(argvs).invoke()


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
  for stmt in prog: print(eval(stmt))
