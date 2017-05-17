# Integ

Note: You need Python 3 and Microsoft Windows to run the Integ interpreter.
  
Integ is an esoteric programming language in which the only datatype is the integer and the only storage is one large, variable-length array of integers which is accessed through non-negative addresses, beginning at 0. In Integ, variables do not get distinct names. Instead, they are accessed with the notation {x and written to with the notation }xy where x is the address number and y is the new integer. y is optional; the program will write 0 to x if y is simply a set of empty parentheses (see below).

Variables are declared in two ways; the variable is always initialized at the same time.

The first declaration method, explicit declaration, occurs simply when a program tries to write to a previously unused address.
So, for instance, a program evaluating }(1)() when storage for address 1 has not yet been allocated will set aside storage for address 0 and set it equal to 0. Similarly, a program evaluating }(5)(7) will set aside storage for address 5 and set it equal to 7.

The second declaration method, implicit declaration, occurs when a program tries to set aside storage for an address that has empty positions between it and the nearest address. For instance, a program evaluating }(5)(7) will not just set aside storage for address 5 and set it equal to 7, but also, if the nearest declared address is 3, set aside storage for 4 and set it equal to 0.

To embed anything inside an operator, use (x). For example, }({(1))() will read from location 1 and write 0 at the location at one's contents. (x) is not counted as an operator, but as a syntax element. Empty () are automatically 0.

Note that addresses cannot be read from unless they have been declared.

Decimal integer constants exist in Integ.

Things can be added and subtracted with + and -, and multiplied and divided with * and /. For instance, +(2)(3) is 5; -(2)(3) is -1; \*(2)(3) is 6; /(2)(3) is 0, as division is rounded down to the nearest integer. The interpreter catches division by zero errors.

To print characters, use ]x. This operator prints the character equivalent to x. For example, ](97) prints "a".
To input a character from the standard input and receive its character code, use [x. x is a dummy argument. Also, note that invalid codes will simply be ignored.

The conditional operator is of the form ?xyz. If x is 0, y will be evaluated; otherwise,
z will be evaluated. For instance, ? (-(\[())(97)) (](97)) () prints "a" if it receives "a", and does not print anything if it receives another character.

The loop operator is of the form \~xy. While x is 0, y will be evaluated. For instance, }()()\~(0)(](}()(+({())(1)))](32)) will print the characters (or try to print the characters) with codes 0, 1, 2, 3, 4, 5... and so forth for infinity, or until the application is exited.

Tabs, spaces, and newlines are ignored; as a result, you can design your code in almost any shape.
