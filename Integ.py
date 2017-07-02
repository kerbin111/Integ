"""2017. By __kerbal__; Unix/MacOS capability by jjthrash.

This program is the reference implementation of the Integ language, version 1.3.

In Integ, the only datatype is the integer. The variables have consecutive addresses in Integ (they may or may not be consecutive in memory) and do not get distinct names. Instead,
they are accessed with the notation {x and written to with the notation }xy where x is the address number and y is the new integer. y is optional;
the program will write 0 to x if y is empty.

Variables are declared in two ways; the variable is always initialized at the same time. 
The first declaration method, explicit declaration, occurs simply when a program tries to write to a previously unused address.
So, for instance, a program evaluating }(1)() when storage for address 1 has not yet been allocated will set aside storage for address 0 and set it equal to 0.
Similarly, a program evaluating }(5)(7) will set aside storage for address 5 and set it equal to 7.

In the second case: 

0 1 2 3 4 5
          ^
          7     

The second declaration method, implicit declaration, occurs when a program tries to set aside storage for an address that has empty positions between it and the
nearest address. For instance, a program evaluating }(5)(7) will not just set aside storage for address 5 and set it equal to 7, but also, if the nearest declared address
is 3, set aside storage for 4 and set it equal to 0.

To embed anything inside an operator, use (x). For example, }({(1))() will read from location 1 and write 0 at the location at one's contents. (x) is not counted
as an operator, but as a syntax feature.

Note that addresses cannot be read from unless they have been declared. The @ operator, which is of the form @(x) where x is a dummy argument, provides the maximum
assigned address to help with storage allocation. If no storage has been allocated, @ outputs -1.
Also note that address numbers must be greater than or equal to 0.

To deallocate storage, use _x. _x will deallocate all storage between the maximum allotted storage address and the address x, so be careful using it.
For example, if 0, 1, and 2 are allocated addresses, _(1) will deallocate 1 and 2, so that the only valid address will become 0.

Integer constants exist in Integ.

Things can be added and subtracted with + and -, and multiplied and divided with * and /. The modulus operator is %.

To print characters, use ]x. This operator prints a numeric code equal to the value of its contents.
To input a character code from the standard input, use [x. Note that [x does not wait for a newline,
and that its implementation may be platform dependent. As a result, this code may not work perfectly
on non-Windows platforms.

To output the current time in seconds since the beginning of the epoch, use "x, where x is a dummy argument. The returned time is rounded down.

To obtain a random number between x and y, use `xy, where x and y are the bounds for the random number. x and y do not have to be in any particular order;
`(0)(10) and `(10)(0) both work. Note that random number generation is intentionally implementation dependent; that way, the implementation determines the level
of randomness used. Note, then, that the implementation is responsible for providing the actual generator and a seed (if your generator is pseudo-random). This
reference implementation uses the Python random module, which is pseudo-random, and its default seed generation settings.

The comparison operator is of the form <ab. If a < b, the operator will return 0; otherwise, it will return 1. This property is diametrically opposed to comparison
behavior in other languages, like C; this is intentional.

The conditional operator is of the form ?xyz. If x is 0, y will be evaluated; otherwise,
z will be evaluated.

The loop operator is of the form ~xy. While x is 0, y will be evaluated.

All operators must have one constitutent character, with the operands following in parentheses.
The character used must be distinct from all other operators' characters.

Comments are of the form #x#, where x can be basically anything. Note that comments of the form #.x.# (which were valid in versions <= 1.1) are no longer valid.
Also note that leaving off the end of a comment at the end of a program is no longer permitted as it was in versions <= 1.1. Comments are removed before code execution and do not nest; as a result,
they may be positioned anywhere within a program, including within an operator definition.

User-defined operators are defined with the form :abc:, where a is the number of operands with which the operator will be called minus one, b is an alphabetical character by which the operator will be called,
and c is the code that will be executed by the operator. There are no parentheses surrounding a, b, and c. The rules surrounding user-defined operators are fairly complex.

Operator definitions are treated similarly to comments; they can be positioned literally anywhere in Integ code as their contents will be noted and removed by the parser before code execution.
operator definitions may be positioned before, after, or even during calls to the operators they define; as a result, Integ does not allow the same operator to be defined multiple times.
Note that because code executed during an interactive shell session is persistent until the session concludes, one must clear the user-defined operators that have already been defined to be able
to redefine them. To do so, one must use , which is not an operator. , behaves very similarly to $, which can be seen below; , which must be written on its own line in the interactive prompt,
will remove all of the user-defined operator definitions. Note that , only works in the interactive prompt, not in regular programs.

As mentioned, the first non-whitespace, non-hash character of an operator definition must be a non-negative integer of operands with which the operator will be called minus one. User-defined operators
must be called with a special operand, the offset operand. As code executed by user-defined operators uses storage, the operator must be provided with an offset, which is basically the first position
on Integ's array of integers that the operator is allowed to access. For instance, if the operator was called with an offset of 5, the operator would only be able to write and read to the array
starting with address 5. Note that the offset is used to calculate relative addresses; to a user-defined operator and its definition, storage starts at 0. For instance, an address that would be considered
address 3 by a user-defined operator called with offset 5 is actually 5 + 3 = absolute address 8. Therefore, if the operator tried to write to address 3, it would actually be writing to absolute address
8 and can be accessed at address 8 outside of the operator.

Certain relative addresses have special significance for a user-defined operator. Relative address 0 is the output address; the value that it holds when the code in the body of the operator definition
finishes executing is the value that the operator will return. Integ automatically writes the value 0 to this relative address when the operator is called; to give it a different value, one must simply
write to it as one would write to a normal location in the body of the operator.

If the user specified a value of a (where :abc:) other than 0 (which is allowed; in this case, the only expected operand is the offset operand), a additional operands will be expected during an operator call.
The values passed to these operands can be accessed by reading from relative storage addresses 1 - a. For instance, if a = 5, the operator will expect 5 operands that will be automatically
written to addresses 1 - 5. The first operand in the call (besides the offset operand, which is not written anywhere) will go to 1, the second to 2, and so forth. 

As mentioned, b in :abc: is the single alphabetical character by which the operator will be called. At the moment, this means that an Integ program may have a maximum of 52 user-defined operators.

c in :abc: is the code that will be executed when the operator is called. All of the regular Integ operators are available, but, as noted, addresses are offset to the starting address defined
in the offset operator. Relative memory address 0 is reserved for output and relative memory addresses 1 - a are reserved for input. One can do what one wants with all other addresses > a , but one should
be careful not to overwrite something important on the tape in the process; remember that relative addresses translate to absolute addresses. All user-defined operators (including the one being defined) are
also available. Recursive calls are possible; however, this reference implementation generates an error if recursion exceeds a certain depth (determined by Python)
because the underlying Python implementation generates an error if recursion exceeds a certain depth. Still, this matter is officially implementation dependent;
implementations where recursion causes no issues are free to allow as much recursion as they wish.

OpPacks (other Integ programs) are imported using the syntax .x. where x is the identification number of the OpPack not surrounded by parentheses. OpPacks are executed and removed (like a comment and an operator definition)
before the program importing the OpPack; as a result, OpPack imports may be placed almost anywhere within a program. Imports do not return a value; however, the OpPack will be executed similarly to a
regular program, so OpPacks can print to output and import other OpPacks. Most usefully, user-defined operators in an OpPack can be used by the importing program, hence the name OpPack.
User-defined operators from OpPacks have the same properties and calling behavior as User-defined operators from the importing program. I recommend (but will not force) OpPack creators to
use uppercase letters for operator characters so that importing programs can at least use the lowercase letters.

The standard library has identification number 0.

To import an OpPack, the Integ interpreter connects to a GitHub repository (called Integ_OpPacks) and finds the file with the name corresponding to the OpPack's identification number.
The file contains a URL to the OpPack's actual location online. Integ retrieves the file at the URL and executes it. Therefore, the following statements are true:

-You must have an internet connection to use OpPacks.

-OpPacks must be retrieved through the Internet, even if you created the OpPack.

Right now, Integbot in the #esoteric-blah freenode IRC channel allows users to add OpPacks to the GitHub and to get info on individual OpPacks.

Overcomments (Comments, Operator definitions, and OpPack imports) are evaluated and removed in this order:

Comments
OpPack imports
Operator definitions

$ can be used within the interactive prompt only to exit. Also note that $ is not an operator, so you can simply write $.
"""

import sys, time, random
import github
import math
from github import Github
from urllib import request
import base64
import codecs

# from http://code.activestate.com/recipes/134892/
class _Getch:
    """Gets a single character from standard input.  Does not echo to the
screen."""
    def __init__(self):
        try:
            self.impl = _GetchWindows()
        except ImportError:
            self.impl = _GetchUnix()

    def __call__(self): return self.impl()


class _GetchUnix:
    def __init__(self):
        import tty, sys

    def __call__(self):
        import sys, tty, termios
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch


class _GetchWindows:
    def __init__(self):
        import msvcrt

    def __call__(self):
        import msvcrt
        return msvcrt.getche()

getch = _Getch()

global numarray #This is the big array that everything reads from.
numarray = [] #Nothing stored in it yet.

global offset #An offset used for relative addressing
offset = 0

def write(arguments):
    """The function that corresponds to the { operator. Takes a list; returns the number written"""
    global offset
    address = int(arguments[0])
    contents = int(arguments[1])
    maxpos = len(numarray) - 1 #The maximum position in the array.

    if address < 0: #We cannot use negative positions.
        print("\nCannot assign negative addresses.")
        sys.exit()
    
    while maxpos < address + offset: #Declaring the storage we need, implicitly and explicitly
        numarray.append(0)
        maxpos += 1

    numarray[address + offset] = contents #Actually writing the info
    return contents

def read(arguments):
    """The function that corresponds to the } operator. Takes a list; returns the number read"""
    global offset
    address = int(arguments[0]) #We trust that parse did its job and properly provided the arguments.
    maxpos = len(numarray) - 1 #The maximum position in the array.

    if address < 0 or (address + offset) > maxpos: #We cannot use negative positions.
        print("\nInvalid address " + str(address) + ".")
        sys.exit()
        
    return numarray[address + offset]

def dealloc(arguments):
    """The function that corresponds to the _ operator. Takes a list; deallocates all addresses between the maximum address and a specified address and returns the address specified."""
    global offset
    address = int(arguments[0])
    maxpos = len(numarray) - 1 #The maximum position in the array.

    if address < 0 or (address + offset) > maxpos: #We cannot use negative positions.
        print("\nInvalid address " + str(address) + ".")
        sys.exit()
        
    del numarray[address : maxpos + 1] #Slicing is weird

    return address
    
def maxa(arguments):
    """The function that corresponds to the @ operator. Takes a dummy list; returns the maximum assigned storage address relative to the local address."""
    global offset
    return len(numarray) - offset - 1

def printer(arguments):
    """The function that corresponds to the ] operator. Takes a list; returns its contents."""
    try:
        #from https://stackoverflow.com/questions/25368786/python-print-does-not-work-in-loop
        #fixes glitch in shell with loop printing
        sys.stdout.write(chr(int(arguments[0])))
        sys.stdout.flush()
    except UnicodeEncodeError:
        pass #We would just print the standard box character that denotes missing
             #character if the character cannot be printed, but that's missing.
             #As a result, we ignore printing the character and just hope no one notices.
    except ValueError:
        pass #This is probably not great practice.
    return arguments[0]

def inputer(arguments):
    """The function that corresponds to the [ operator.
       Takes a dummy list; returns a character code where the character is from the standard input."""

    return ord(getch())

def add(arguments):
    """The function that corresponds to the + operator. Takes a list; returns the sum of its operands."""
    return int(arguments[0] + arguments[1])

def subtract(arguments):
    """The function that corresponds to the - operator. Takes a list; returns the difference between the first and second operands."""
    return int(arguments[0] - arguments[1])

def multiply(arguments):
    """The function that corresponds to the * operator. Takes a list; returns the product of its operands."""
    return int(arguments[0] * arguments[1])

def divide(arguments):
    """Of the form /xy, with x and y in parentheses. Returns, using truncation division, x / y, discarding the remainder."""
    
    if not arguments[1]:
        c.connection.privmsg(channel, author + ": Cannot divide by zero.")
        sys.exit()
    
    div = abs(arguments[0]) // abs(arguments[1]) #Performs truncation division

    if arguments[0] * arguments[1] >= 0:
        return int(div)
    else:
        return int(div * -1)
    
def modulus(arguments):
    """Of the form %xy, with x and y in parentheses. Returns, using truncation division, the remainder of x / y."""
    
    if not arguments[1]:
        c.connection.privmsg(channel, author + ": Cannot divide by zero.")
        sys.exit()
    return  arguments[0] - arguments[1] * divide([arguments[0], arguments[1]]) #(Thanks to wob_jonas)

def inttime(arguments):
    """The function that corresponds to the " operator, Takes a list; returns the time in seconds since the start of the epoch, rounded down."""
    return int(time.time())

def randomint(arguments):
    """The function that corresponds to the ` operator. Takes a list (namely, the bounds; they do not have to be in order)
    and returns the random number between the bounds, inclusive."""
    if arguments[0] > arguments[1]:
        return random.randint(arguments[1], arguments[0])
    return random.randint(arguments[0], arguments[1])

def comp(arguments):
    """The function that corresponds to the < operator. Takes a list (namely, a and b)
    and returns 0 if a < b and 1 otherwise."""

    a = arguments[0]
    b = arguments[1]

    if a < b:
        return 0
    else:
        return 1

def conditional(arguments):
    """conditional is a dummy function for ?. metaparse handles conditional execution."""
    if arguments:
        return arguments[0]

def loop(arguments):
    """conditional is a dummy function for ~. metaparse handles loop execution."""
    if arguments:
        return arguments[0]

def parse(inputstr, opconst):
    """Parses an input string according to the operator character list opconst
       and outputs, in this order, the operator, the operands, and anything else. The number of repeated
       characters in opconst determines whether an operator is unary, binary, tertiary, etc."""

    inputstr = inputstr.replace(" ", "") #Removes all notable types of whitespace
    inputstr = inputstr.replace("\n", "")
    inputstr = inputstr.replace("\t", "")
    
    opconst0 = "" #Gets first characters of operators
    for i in opconst:
        opconst0 += i[0]

    j = 0
    pos = 0 #The current position in the string
    
    operator = None

    if inputstr[0] == ")" or inputstr[0] == "(":
        print("\nError: Illegal use of ().")
        sys.exit()
    for i in opconst0: #Gets the operator type
        
        if i == inputstr[0]:
            operator = opconst[j]
            pos += 1
            break
        
        j += 1

    if inputstr[0] == "$":
        print("\n$ is not an operator; type it by itself in the interactive shell to exit.")
        sys.exit()

    if inputstr[0] == "," and not sys.stdin.isatty():
        print("\n, is not an operator; type it by itself in the interactive shell to clear the user-defined operator definitions.")
        sys.exit()

    if inputstr[0] == "," and sys.stdin.isatty():
        print("\nClearing user defined operator definitions.")
        sys.exit()
    
    if not operator: #We should have found an operator.
        print("\nOperator " + inputstr[0] + " not found.")
        sys.exit()
    lparen = rparen = tlp = trp = 0 #The first two are reset every argument; the last two stick around 

    j = 0

    args = []
    
    while j < len(operator): #Now we use j to get the arguments
        
        temparg = ""
        lparen = rparen = 0

        if pos > (len(inputstr) - 1):
            break
        
        for i in inputstr[pos:]: #Getting the arguments
            
            if lparen > rparen and (i != ")" or lparen - 1 != rparen):
                #Only add the character if the parentheses are still unbalanced. Do not add parentheses
                #that balance the parentheses
                temparg += i

            if lparen == rparen and lparen: #If the parentheses are balanced and exist:
                break

            if not lparen and not rparen and i != "(" and i != ")" and len(args) < len(operator):
                print("\nMore operands expected.")
                sys.exit()
            if i == "(":
                lparen += 1
                tlp += 1
        
            if i == ")":
                rparen += 1
                trp += 1
                
            pos += 1

        if len(args) < len(operator): #We don't want extra arguments
            args.append(temparg)
        else:
            break

        
        j += 1

    if len(args) < len(operator):
        print("\nMore operands expected.")
        sys.exit()
    if tlp != trp: #If the parentheses were never balanced completely in the string
        print("\nParentheses not balanced.")
        sys.exit()
    return [operator, args, inputstr[pos:]] #We return the operator, its arguments, and anything left in the string.

def metaparse(inputstring):
    """metaparse is responsible for making parse helpful. parse separates a string into its components,
       and metaparse is responsible for using parse and figuring out how those components work together.
       Unlike parse, metaparse takes a global dictionary with keys as parse-formatted operator strings and
       values as functions that metaparse must call. metaparse passes the keys to parse."""
    global opdict
    
    remainder = ""
    
    if not inputstring: #Returns 0 if the string is empty.
        return 0, remainder
    
    integer = 0
    try: #We try to convert the input string into an integer and return the integer. If that fails,
         #We know that we need to parse the input more.
        integer = int(inputstring)
        return integer, remainder
    except ValueError:
        pass

    output = parse(inputstring, list(opdict.keys())) #Get and unpack parse output
    
    op = output[0]
    arguments = output[1]
    remainder = output[2]

    function = opdict[op] #The function to be executed from the operator
    parsedvals = [] #parsing the arguments

    if op == "???": #metaparse directly works with the conditional operator
        
        if metaparse(arguments[0])[0] == 0:
            parsedvals.append(metaparse(arguments[1])[0])
            
        else:
            parsedvals.append(metaparse(arguments[2])[0])
        
    elif op == "~~": #metaparse works directly with the loop operator
        
        while metaparse(arguments[0])[0] == 0:
            completed = metaparse(arguments[1])[0]
            parsedvals.append(completed)
        try: #If the loop never evaluates, the loop body is defined to return 0
            completed
        except NameError:
            parsedvals.append(0)
    
    else: #everything else ultimately goes through functions
        for i in arguments:
            parsedvals.append(metaparse(i)[0])
    
    out = function(parsedvals)
    if remainder:
        out = metaparse(remainder)[0]
    
    return out, remainder

def nocomments(inputstr):
    """nocomments removes comments, which are of the form #<comment_text># and which do not nest.
       You don't have to put a comment end signifier if you want the last bit of the program to be a comment."""
    incomment = False
    lastchar = None
    output = ""
    for i in inputstr: #Basically, just add characters to the output if they aren't in comments in the input.
        if i == "#":
            incomment = not incomment
                    
        if not incomment and i != "#":
          output += i

        lastchar = i

    if incomment:
        print("Comment not terminated with closing #")
        sys.exit()

    return output

def find_func(inputstr):
    """find_func finds user function definitions in Integ code, parses and saves them to memory (not storage),
    and deletes the definition so that metaparse can use it."""
    global opdict
    
    indef = False

    inopnum = True

    opchar = None

    functbody = ""

    output = ""

    opnum = -1

    #A user-defined function executed during metaparse
    
    
    for i in inputstr:
        if i == ":": #We try to find the bounds of a definition
            indef = not indef

            if not indef:
                #What follows is some slightly confusing programming used to create a user-defined operator function and add it to the opdict

                if not opchar:
                    print("\nThe first non-digital, non-whitespace character of an operator definition must be a single alphabetical operator designator character.")
                    sys.exit()
                
                exec("def " + opchar + """function(arguments):
                    global offset
                    offset = arguments[0]
                    
                    args = arguments[1:]
                    metaparse(\"}()()\")
                    count = 1
                    while count <= len(args):
                        metaparse(\"}(\" + str(count) + \")(\" + str(args[count - 1]) + \")\")
                        count += 1
                    metaparse(\"""" + functbody.replace("\"", "\\\"") + """\")
                    results = metaparse(\"{()\")[0]
                    offset = 0
                    return (results)""")
                    
                exec("opdict[opchar*(opnum + 1)] = " + opchar + "function")

                functbody = ""
                opnum = -1
                indef = False
                inopnum = True
                opchar = None

            continue

        if not indef and i != ":":
          output += i

        if indef:
            if inopnum:
                if opnum == -1:
                    try:
                        opnum = int(i)
                    except ValueError:
                        print("\nValid number of operands not provided.")
                        sys.exit()
                else:
                    try:
                        opnum = opnum * 10 + int(i) #We collect the ints
                    except ValueError:
                        if opnum < 0:
                            print("\nOperators must have a nonnegative number of arguments, including the mandatory memory allocation argument.")
                            sys.exit()
                        inopnum = False 
                        if i.isalpha(): #We try to get the operator character, which must be a single alphabetical character
                            opconst0 = "" #Gets first characters of operators
                            for j in opdict.keys():
                                opconst0 += j[0]
                            if i in opconst0:
                                print("\nMultiple conflicting operator definitions provided. New definition not used.")
                                sys.exit()
                            opchar = i
                        else:
                            print("\nThe first non-digital character of an operator definition must be a single alphabetical operator designator character.")
                            sys.exit()

            else:
                if i != ":":
                    functbody += i 

    if indef:
        print("Operator definition not terminated with closing :")
        sys.exit()
    return output
            

def find_pack(inputstr):
    """find_pack finds OpPack imports in Integ code, executes the corresponding file,
    and deletes the definition so that metaparse can use it."""

    global oppacks
    
    inimport = False

    output = ""
    importbody = ""
    
    for i in inputstr: #Basically, just add characters to the output if they aren't in definitions in the input.
        if i == ".":
            inimport = not inimport

            if not inimport:
                
                try:
                    importnum = int(importbody) #We get the integer that refers to the OpPack
                except ValueError:
                    print("OpPack imports only contain a single, non-negative integer. This integer identifies the OpPack to be imported.")
                    sys.exit()
                    
                if importnum < 0:
                    print("OpPack imports only contain a single, non-negative integer. This integer identifies the OpPack to be imported.")
                    sys.exit()

                try: #Trying to get the URL of the OpPack; you have to decode it
                    pack = codecs.decode(base64.b64decode(oppacks.get_file_contents(str(importnum)).content))
                except:
                    print("OpPack " + str(importnum) + " may not exist, or there may be connection errors. Opening failed.")
                    sys.exit()

                try: #Trying to get the OpPack
                    file = request.urlopen(pack)
                except:
                    print("OpPack " + str(importnum) + " could not be opened.")
                    sys.exit()

                script = codecs.decode(file.read())
                
                execute(script.replace(" ", "").replace("\n", "").replace("\t", "").replace("\r", ""))
                
                file.close()
                
                importbody = ""

                

        if inimport and i != ".":
            importbody += i
                    
        if not inimport and i != ".":
          output += i

    if inimport:
        c.connection.privmsg(channel, author + ": Import not terminated with closing .")
        sys.exit()

    return output


#The main body of the interpreter--almost like a metametaparse function

githubac = Github()

global oppacks
oppacks = None

useops = True

try:
    oppacks = githubac.get_repo("kerbin111/Integ_OpPacks")
except:
    print("Couldn't access the Github repo. Integ will ignore any OpPack imports.")
    useops = False


global opdict
opdict = {"}}" : write, "{" : read, "_" : dealloc, "@" : maxa, "]" : printer, "[" : inputer, "++" : add, "--" : subtract,
          "**" : multiply, "//" : divide, "%%" : modulus, "\"" : inttime, "``" : randomint, "<<" : comp, "???" : conditional, "~~" : loop}
                                             #These are the operators currently supported by Integ. The number
                                             #of times that the character is repeated is the number of operands
                                             #that the operator requires. Each operator (except for the conditional and loop operators)
                                             #maps to a function that
                                             #performs its task.

def execute(string1 = None):
    
    if string1:
        
        try:
            partial = nocomments(string1.replace(" ", "").replace("\n", "").replace("\t", ""))
            
            if useops:
                metaparse(find_func(find_pack(partial)))
            else:
                metaparse(find_func(partial))
            
        except KeyboardInterrupt:
                print("\nKeyboard Interrupt.")
        except RecursionError:
                print("\nImplementation-Specific Error: Recursion limit exceeded.")
        except SystemExit:
            if sys.stdin.isatty():
                pass
            else:
                sys.exit()

        return

    string = "" #The actual program is stored here
    
    if (sys.stdin.isatty()):
        print("""
    --------Integ 1.3---------
     Interactive  Interpreter""")
        while True: #interactive interpreter
            
            print("\n")
            
            string = input(">>> ").replace(" ", "").replace("\n", "").replace("\t", "")
            if string == "$":
                break
            if string == ",":
                keys = opdict.copy().keys()
                for i in keys:
                    if i.isalpha():
                        opdict.pop(i) #Basically, this gets rid of user-defined operators
            try:
                partial = nocomments(string.replace(" ", "").replace("\n", "").replace("\t", ""))
                if useops:
                    metaparse(find_func(find_pack(partial)))
                else:
                    metaparse(find_func(partial))
            except SystemExit:
                pass #We don't want to exit when there's an error.
            except RecursionError:
                print("\nImplementation-Specific Error: Recursion limit exceeded.")
            except KeyboardInterrupt:
                print("\nKeyboard Interrupt.")
                continue
    else:
        while True: #collecting input for redirection-type input
            try:
                string += input()
            except EOFError:
                break
        try:
            partial = nocomments(string.replace(" ", "").replace("\n", "").replace("\t", ""))
            if useops:
                metaparse(find_func(find_pack(partial)))
            else:
                metaparse(find_func(partial))
            
        except KeyboardInterrupt:
                print("\nKeyboard Interrupt.")
        except RecursionError:
                print("\nImplementation-Specific Error: Recursion limit exceeded.")
            
execute()
