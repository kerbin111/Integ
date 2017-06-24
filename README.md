
# Integ

### Version 1.2

*"An esoteric programming language composed of nothing but parentheses"
            -rdococ*

Note: You need Python 3 to run the Integ interpreter.

Integ is an esoteric programming language in which the only datatype is the integer and the only storage is one large, variable-length array of arbitrary-precision integers which is accessed through non-negative addresses, beginning at 0. In Integ, variables do not get distinct names. Instead, they are accessed with the notation {x and written to with the notation }xy
where x is the address number and y is the new integer. y is optional; the program will write 0 to x if y is simply a set of empty parentheses (see below). Note that }xy returns x.

Variables are declared in two ways; the variable is always initialized at the same time.

The first declaration method, explicit declaration, occurs simply when a program tries to write to a previously unused address.
So, for instance, a program evaluating }(1)() when storage for address 1 has not yet been allocated will set aside storage for address 0 and set it equal to 0. Similarly, a program evaluating }(5)(7) will set aside storage for address 5 and set it equal to 7.

The second declaration method, implicit declaration, occurs when a program tries to set aside storage for an address that has empty positions between it and the nearest address. For instance, a program evaluating }(5)(7) will not just set aside storage for address 5 and set it equal to 7, but also, if the nearest declared address is 3, set aside storage for 4 and set it equal to 0.

To embed anything inside an operator, use (x). For example, }({(1))() will read from location 1 and write 0 at the location at one's contents. (x) is not counted as an operator, but as a syntax element. Empty () are automatically 0.

Note that addresses cannot be read from unless they have been declared. The @ operator, which is of the form @x where x is a dummy argument, provides the maximum
assigned address to help with storage allocation. If no storage has been allocated, @ outputs -1.
Also note that address numbers must be greater than or equal to 0.

To deallocate storage, use _x. _x will deallocate all storage between the maximum allotted storage address and the address x, so be careful using it. _x returns x.
For example, if 0, 1, and 2 are allocated addresses, _(1) will deallocate 1 and 2, so that the only valid address will become 0. 

\Decimal integer constants exist in Integ.

Things can be added and subtracted with + and -, and multiplied and divided with * and /. Division remainders may be obtained with the modulus operator, which is %. For instance, +(2)(3) is 5; -(2)(3) is -1; *(2)(3) is 6; /(2)(3) is 0, as Integ uses truncated division and modulus. The interpreter catches division by zero errors.

To print characters, use ]x. This operator prints the character equivalent to x. For example, ](97) prints "a". ]x returns x.
:To input a character from the standard input and receive its character code, use [x, where x is a dummy argument. Note that invalid codes will simply be ignored. [ does not work in IDLE; use a command line interface instead.

To output the current time in seconds since the beginning of the epoch, use "x, where x is a dummy argument. The returned time is rounded down.

To obtain a random number between x and y, use \`xy, where x and y are the bounds for the random number. x and y do not have to be in any particular order;
\`(0)(10) and \`(10)(0) both work. Note that random number generation is intentionally implementation dependent; that way, the implementation determines the level
of randomness used. Note, then, that the implementation is responsible for providing the actual generator and a seed (if your generator is pseudo-random). This
reference implementation uses the Python random module, which is pseudo-random, and its default seed generation settings.

The comparison operator is of the form <ab. If a < b, the operator will return 0; otherwise, it will return 1. This property is diametrically opposed to comparison behavior in other languages, like C; this is intentional.
The conditional operator is of the form ?xyz. If x is 0, y will be evaluated; otherwise,
z will be evaluated. For instance, ? (-(\[())(97)) (](97)) () prints "a" if it receives "a", and does not print anything if it receives another character.

The loop operator is of the form \~xy. While x is 0, y will be evaluated. If x is never 0, then the loop will simply return 0. For instance, }()()\~(0)(](}()(+({())(1)))](32)) will print the characters (or try to print the characters) with codes 0, 1, 2, 3, 4, 5... and so forth for infinity, or until the application is exited.

Tabs, spaces, and newlines are ignored; as a result, you can design your code in almost any shape.

Comments are of the form #x#, where x can be basically anything. Note that comments of the form #.x.# (which were valid in versions <= 1.1) are no longer valid.
Also note that leaving off the end of a comment at the end of a program is no longer permitted as it was in versions <= 1.1. Comments are removed before code execution and do not nest; as a result,
they may be positioned anywhere within a program, including within an operator definition.

User-defined operators are defined with the form ::abc::, where a is the number of operands with which the operator will be called minus one, b is an alphabetical character by which the operator will be called,
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

If the user specified a value of a (where ::abc::) other than 0 (which is allowed; in this case, the only expected operand is the offset operand), a additional operands will be expected during an operator call.
The values passed to these operands can be accessed by reading from relative storage addresses 1 - a. For instance, if a = 5, the operator will expect 5 operands that will be automatically
written to addresses 1 - 5. The first operand in the call (besides the offset operand, which is not written anywhere) will go to 1, the second to 2, and so forth. 

As mentioned, b in ::abc:: is the single alphabetical character by which the operator will be called. At the moment, this means that an Integ program may have a maximum of 52 user-defined operators.

c in ::abc:: is the code that will be executed when the operator is called. All of the regular Integ operators are available, but, as noted, addresses are offset to the starting address defined
in the offset operator. Relative memory address 0 is reserved for output and relative memory addresses 1 - a are reserved for input. One can do what one wants with all other addresses > a , but one should
be careful not to overwrite something important on the tape in the process; remember that relative addresses translate to absolute addresses. All user-defined operators (including the one being defined) are
also available. Recursive calls are possible; however, this reference implementation generates an error if recursion exceeds a certain depth (determined by Python)
because the underlying Python implementation generates an error if recursion exceeds a certain depth. Still, this matter is officially implementation dependent;
implementations where recursion causes no issues are free to allow as much recursion as they wish.

$ can be used within the interactive prompt only to exit. Also note that $ is not an operator, so you can simply write $.

----
Examples
----

helloworld.int: Prints "hello, world".

numiter.int: Prints numbers 0-9 forwards and backwards endlessly.

quine.int: A quine by wob_jonas from the #esoteric IRC community.

say_a.int: Wants you to press "a" over and over and over. This program does not work in the Python IDLE; try a command prompt instead.
