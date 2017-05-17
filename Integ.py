"""2017 Joshua Fitzgerald

This program is the reference implementation of the Integ language for Windows. To port the program,
I suspect that you simply need to change inputer and the msvcrt import.

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
as an operator, but as a syntax feature (or something; I don't know).

Note that addresses cannot be read from unless they have been declared.
Also note that address numbers must be greater than or equal to 0.

Integer constants exist in Integ.

Things can be added and subtracted with + and -, and multiplied and divided with * and /.

To print characters, use ]x. This operator prints a numeric code equal to the value of its contents.
To input a character code from the standard input, use [x. Note that [x does not wait for a newline,
and that its implementation may be platform dependent. As a result, this code may not work perfectly
on non-Windows platforms.

The conditional operator is of the form ?xyz. If x is 0, y will be evaluated; otherwise,
z will be evaluated.

The loop operator is of the form ~xy. While x is 0, y will be evaluated.

All operators must have one constitutent character, with the operands following in parentheses.
The character used must be distinct from all other operators' characters."""

import sys
import msvcrt #Change if you are on a non-Windows OS

global numarray #This is the big array that everything reads from.
numarray = [] #Nothing stored in it yet.

def write(arguments):
    """The function that corresponds to the { operator. Takes a list; returns the number written"""
    address = int(arguments[0])
    contents = int(arguments[1])
    maxpos = len(numarray) - 1 #The maximum position in the array.

    if address < 0: #We cannot use negative positions.
        sys.exit("Cannot assign negative addresses.\n")
    
    while maxpos < address: #Declaring the storage we need, implicitly and explicitly
        numarray.append(0)
        maxpos += 1

    numarray[address] = contents #Actually writing the info
    
    return contents

def read(arguments):
    """The function that corresponds to the } operator. Takes a list; returns the number read"""
    address = int(arguments[0]) #We trust that parse did its job and properly provided the arguments.
    maxpos = len(numarray) - 1 #The maximum position in the array.

    if address < 0 or address > maxpos: #We cannot use negative positions.
        sys.exit("Invalid address " + str(address) + ".\n")
    
    return numarray[address]

def printer(arguments):
    """The function that corresponds to the ] operator. Takes a list; returns its contents."""
    try:
        print(chr(int(arguments[0])), end = "")
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

    return ord(msvcrt.getche())

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
    """The function that corresponds to the - operator. Takes a list; returns the quotient the first and second operands."""
    if not arguments[1]:
        sys.exit("Cannot divide by zero.\n")
    return int(arguments[0] / arguments[1])

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
        sys.exit("Error: Illegal use of ().\n")
    
    for i in opconst0: #Gets the operator type
        
        if i == inputstr[0]:
            operator = opconst[j]
            pos += 1
            break
        
        j += 1

    if not operator: #We should have found an operator.
        sys.exit("Operator " + inputstr[0] + " not found.\n")
    
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
                sys.exit("More operands expected.\n")
        
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
        sys.exit("More operands expected.\n")
    
    if tlp != trp: #If the parentheses were never balanced completely in the string
        sys.exit("Parentheses not balanced.\n")
        
    return [operator, args, inputstr[pos:]] #We return the operator, its arguments, and anything left in the string.

def metaparse(inputstring, operators):
    """metaparse is responsible for making parse helpful. parse separates a string into its components,
       and metaparse is responsible for using parse and figuring out how those components work together.
       Unlike parse, metaparse takes a dictionary with keys as parse-formatted operator strings and
       values as functions that metaparse must call. metaparse passes the keys to parse."""

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
,
    output = parse(inputstring, list(operators.keys())) #Get and unpack parse output
    op = output[0]

arguments = output[1]
    remainder = output[2]

    function = operators[op] #The function to be executed from the operator
    parsedvals = [] #parsing the arguments

    if op == "???": #metaparse directly works with the conditional operator
        
        if metaparse(arguments[0], operators)[0] == 0:
            parsedvals.append(metaparse(arguments[1], operators)[0])
            
        else:
            parsedvals.append(metaparse(arguments[2], operators)[0])
        
    elif op == "~~": #metaparse works directly with the loop operator
        
        while metaparse(arguments[0], operators)[0] == 0:
            parsedvals.append(metaparse(arguments[1], operators)[0])
    
    else: #everything else ultimately goes through functions
        for i in arguments:
            parsedvals.append(metaparse(i, operators)[0])

    out = function(parsedvals)
    if remainder:
        out = metaparse(remainder, operators)
    return out, remainder

def nocomments(input):
    """nocomments removes comments, which are of the form #.<comment_text>.# and which do not nest.
       You don't have to put a comment end signifier if you want the last bit of the program to be a comment."""
    incomment = False
    lastchar = None
    output = ""
    for i in input: #Basically, just add characters to the output if they aren't in comments in the input.
        if i == "." and lastchar == "#" and incomment == False:
            incomment = True
        if i == "#" and lastchar == "." and incomment == True:
            incomment = False
                    
        if not incomment:
          output += i

        lastchar = i
    
    return output

#The main body of the interpreter--almost like a metametaparse function

string = "" #The actual program is stored here
opdict = {"}}" : write, "{" : read, "]" : printer, "[" : inputer, "++" : add, "--" : subtract,
          "**" : multiply, "//" : divide, "???" : conditional, "~~" : loop}
                                             #These are the operators currently supported by Integ. The number
                                             #of times that the character is repeated is the number of operands
                                             #that the operator requires. Each operator (except for the conditional and loop operators)
                                             #maps to a function that
                                             #performs its task.

while True: #collecting input
    try:
        string += input()
    except EOFError:
        break

metaparse(nocomments(string), opdict)
