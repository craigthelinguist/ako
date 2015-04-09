

## Types.
## ------------------------------------------------------------

Symbol = str
List = list
Number = (int, float)

class Env(dict):

    def __init__(self, vars, vals, parent):
        '''
        :param vars: names of variables in this environment.
        :param vals: values of variables in this environment.
        :param parent: the environment which spawned this one.
        :return:
        '''
        for var,val in zip(vars,vals):
            self[var] = val
        self.parent = parent

    def valueOf(self, var):
        '''
        Look for the value of var. If it cannot be found, look at
        the parent environment.
        :param var: name of a binding you want the value of.
        :return: value of the binding.
        '''
        if var in self: return self[var]
        if self.parent == None: raise ValueError("Unknown variable: " + var)
        return self.parent.valueOf(var)

class Func(object):

    def __init__(self, args, body, env):
        self.args = args
        self.body = body
        self.env = env

    def invoke(self, *args):
        '''
        Apply this function to the specified arguments.
        :param args: values to bind to the arguments of this function.
        :return: evaluation of this function.
        '''
        return eval(self.body, Env(self.args, args, self.env))


## Lexer/parser.
## ------------------------------------------------------------

def tokenise(program):
  return program.replace("(", " ( ").replace(")"," ) ").split()

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

STD_ENV = Env(["true", "nil"], ["true", "nil"], None)

## Interpreter.
## ------------------------------------------------------------

def eval(expr, env):

  # evaluate literals

  if type(expr) in Number:
    return expr
  elif isinstance(expr, Symbol):
    return env.valueOf(expr)

  # otherwise check what the expression is.
  fst = expr[0]

  # return the literal expression.
  if fst == "quote": return expr[1]

  elif fst.startswith("'"): return fst[1:]

  # return true if it is a symbol.
  elif fst == "atom":
    return "true" if isinstance(expr[2], Symbol) else []

  elif fst == "<":
      return "t" if eval(expr[1], env) < eval(expr[2], env) else "nil"

  elif fst == ">":
      return "true" if eval(expr[1], env) > eval(expr[2], env) else "nil"

  elif fst == ">=":
      return "true" if eval(expr[1], env) >= eval(expr[2], env) else "nil"

  elif fst == "<=":
      return "true" if eval(expr[1], env) >= eval(expr[2], env) else "nil"

  elif fst == "cond":
      for cond, value in expr[1:]:
          if eval(cond, env) != "nil": return eval(value, env)
      raise ValueError("Incomplete conditional")

  # test equality of two expressions
  elif fst in ["eq", "="]:
      return "true" if eval(expr[1], env) == eval(expr[2], env) else "nil"

  # car returns the head of a list.
  elif fst == "car":
      return expr[1][0]

  # return everything except the head of a list
  elif fst == "cdr":
      return expr[1][1:]

  # prepend element to list
  elif fst == "cons":
      return [expr[1]] ++ expr[2]

  # arithmetic operations
  elif fst in ["+", "add"]:
      return eval(expr[1], env) + eval(expr[2], env)
  elif fst in ["-", "sub"]:
      return eval(expr[1], env) - eval(expr[2], env)
  elif fst in ["*", "mul"]:
      return eval(expr[1], env) * eval(expr[2], env)
  elif fst in ["/", "div"]:
      return eval(expr[1], env) / eval(expr[2], env)

  # successor of the expression
  elif fst == "succ":
      return eval(expr[1], env) + 1

  # predecessor of the expression
  elif fst == "pred":
      return eval(expr[1], env) - 1

  # variable binding
  elif fst == "def":
      name, body = expr[1], expr[2]
      env[name] = eval(body, env)

  # lambda is for defining function literals
  elif fst == "lambda":
      return Func(expr[1], expr[2], env)

  elif fst == "import":
      for fname in expr[1:]:
          eval_prog(fname, env)

  # function/variable invocation
  else:
    fn = eval(expr[0], env)
    if not isinstance(fn, Func): return fn
    argvs = [eval(arg, env) for arg in expr[1:]]
    return fn.invoke(*argvs)


def eval_prog(fname, env):
    if not fname.endswith(".ako"): raise ValueError("Must specify .ako file")
    with open(fname) as f: prog = f.read()
    prog = parse(prog)
    for stmt in prog:
        val = eval(stmt, env)
        if val != None: print(val)


## Main.
## ------------------------------------------------------------
import sys

if __name__ == "__main__":
  fname = sys.argv[1]
  eval_prog(fname, STD_ENV)
