# Easyparse

Easyparse is a command line argument parser. It is extremely lightweight.
It has no external dependencies. Easyparse can not only handle the argument
parsing in your programs, but it can also handle displaying basic help screens
and error-handling. It's significantly easier to use than other argument parsers,
as it favours simplicity over complexity or advanced features.

## Setup & Prerequsites

- `python 3.6` or above
- `pip`

Start by installing the module using pip.
```shell
$ python3 -m pip install easyparse
```

## Initialising

In your program, import the module, then create an instance of the opt_parser class.
```Python
import easyparse

parser = easyparse.opt_parser()
```

From this point forward, we will use our `parser` instance to demonstrate
any features or examples.

The opt_parser accepts two optional flags.
`parser = easyparse.opt_parser(argument_list=sys.argv, show_colors=True)`

The `argument_list` flag takes a list. This is where the arguments will be
parsed from. By default this is sys.argv. For most programs this is where
you will want to take the arguments in from, but you are free to use any
list you wish.

The `show_colors=True` flag can be set to True or False, depending on
whether you want to enable the default colours when displaying the help
screen, displaying errors and such. Unless your terminal doesn't support
colour, there is usually no reason to turn this setting off.

## Adding arguments

Easyparse works by you first adding arguments, then calling the `parse_args` function
which then looks at `argument_list` and parses the arguments from that list. Therefore,
to start parsing arguments, you must first add the arguments that you are looking to parse.

```Python
parser.add_arg("<short_form>", "<long_form>", "<meta_var>", "<Description>", <optional=True/False>)
```

Here's an example of how you would add the default help argument.

```Python
parser.add_arg("-h", "--help", None,"Show this help screen and exit.", optional=True)
```
To add an argument, you have to add the short form, for it to count as a valid argument.
Now you may wonder, ***'what if I wish to add an argument that only has a short form and but
lacks one or more of the other variables?'***

This can be easily achieved by inserting a `None` in the position of the variable,
or explicitly specifying what the variable is representing like this `variable=value`
For example, if I wanted to add such an argument that doesn't require one or more values,
I could do it like these few examples.

```Python
parser.add_arg("-s", None, None, "Turn on some option.", optional=True)
parser.add_arg("-n", "--no-foobar", None, "Turn off some other option.")
parser.add_arg("-f", None, "file", description="Read values from file.")
parser.add_arg("-c", meta_var="ciphertext", description="Lorem ipsum dolor sit amet.")
parser.add_arg("-v", "--version", description="Lorem ipsum dolor sit amet.")
```

Easyparse is quite flexible, as to what characters can be used as long as
the argument follows a certain format. **Short hand arguments need to
start with `-` and have only character after that.** The character can
be an alphabet or punctuation mark like `-?`, or it can be any single digit number,
`-1`. **Full form arguments need to start with `--` and can be of any length
containing any printable characters.**

The only exception to this is the final variable `optional=False`.
You don't have to specify this option, unless you wish to mark the
argument as optional. When you display the help screen, it will show
up under the `Optional arguments` section.

## Adding comments

After adding all the arguments, you may wish to add some comments,
to describe how your program works, or to convey other information
to the user. These comments will be displayed alongside the usage
option in the help screen, when the help screen is called.
Adding a comment is quite simple, using our `parser` instance,
it can be done like this.

```Python
parser.add_comment("Hey, look at me, I'm a comment!")
parser.add_comment("I'm another comment. Cool, huh?")
```

## Adding examples

Like comments, you can add usage examples, that will show
up at the top of the help screen. **Note: You do not
need to specify the file-name when adding examples,
it will be prepended automatically**. You can override
this behaviour by specifying a string, ideally a filename,
in the second variable, if you wish. You can add examples like this.

```Python
parser.add_example("-s -e -i foo -k bar")
parser.add_example("-d -n 32 -r 128 -i 'Lorem ipsum dolor' ")
parser.add_example("<example>", prepend_name="<file-name>")
parser.add_example("./file-name <example>", str()) # Nothing prepended
```

## Parsing arguments

Once we have setup our arguments, we need to parse them.
Let's use the same `parser` instance as above.

```Python
parser.parse_args()
```

Once the `parse_args` function is called the arguments will be parsed
and a dictionary will be created. This will allow you to see which
specific arguments have been set and obtain values from arguments
which need a value passed to it. It is at this point, that if any
errors have been detected. It will display an error and exit showing
which error it encountered and with which argument.

## Checking presence

To check if an argument has been supplied, we can use the `is_present`
function. You can use either the short form or long form of the
argument to check presence. The function will return `True` if
the argument is set. If the argument is not set, it will return
`None`. *Note: In some cases it could return False instead of None.
This shouldn't happen, but if it does, please report this as an issue,
stating which arguments you supplied for it to cause this.*

```Python
# Check if the help flag is set
# Any form can be used. Both will result
# In True if present.

foo = parser.is_present("-h")
bar = parser.is_present("--help")
other_option = parser.is_present("-v")
nonexistent_option = parser.is_present("-z")


print(foo)
print(bar)
print(other_option)
print(nonexistent_option)
```

Let's invoke our program with -h

```shell
$./program -h
True
True
None
None

$./program -v
None
None
True
None
```

Once we have checked presence, we need to get the values
from the present arguments, which we can use to create
a functional program.

## Checking multiple

Imagine having to do `parser.is_present()` for every
argument you want to check. That would get redundant
very quickly. Fortunately, with the `check_multiple`
function. `check_multiple` takes any number of arguments
with a final value called `sep`

To check if multiple arguments are present, we can
do this.

```Python
parser.check_multiple("-s", "-e", "-i", "-k")
```
It doesn't matter if the argument is the short hand or
the long form. It will either return `True` if all
the arguments have been supplied or it will return
`False` if one or more are not supplied.

You may also be wondering, ***What if I wanted to
see presence for each argument manually?***
That's where the `sep=<True/False>` comes in.
if `sep` is set to `True` a list will be returned
containing a `True/False` depending on whether the argument
is present, instead of a boolean value. We can achieve this
in the examples following.

```Python
parser.check_multiple("-s", "-x", "-f", "-k", sep=True)
```

Let's create a small demonstration, using our `parser`
instance from earlier.

```Python
x = parser.check_multiple("-s", "-e", "-i", "-k")
y = parser.check_multiple("-s", "-x", "-f", "-k", sep=True)
print(x)
print(y)
```

Let's run our program with some arguments and verify
that it works.

```shell
./program -se -i "lorem ipsum" -k "dolor sit amet"
True
[True, False, False, True]
```

## Getting values

The whole purpose of an argument parser is so we can pick
up supplied values. We can do that easily here, like this.

```Python
input_value = parser.value_of("-i")
nonexistent_value = parser.value_of("-f")

print("You said: ", input_value)
print("This should return be None: ", non_existent_value)
```

Let's test it out.

```shell
$./program -i 'Hello!'
You said Hello!
This should be None: None
```

## Help screen

In programs which you require the user to supply command-line
arguments, chances are, you would need a help screen, to
display the possible arguments your program can take.
Easyparse makes this process quite simple. Every time you
add an argument, it automatically gets added to the help
screen. All you need to do is simply display that screen when
you want, perhaps when the user supplies `-h` or `--help`.

```Python
#Let's create a small program to demo this.
#program.py

import sys
import easyparse
parser = easyparse.opt_parser()

parser.add_arg("-h", "--help", None,"Show this help screen and exit.", optional=True)
parser.add_arg("-v", "--version", None,"Print version information and exit.", optional=True)
parser.add_arg("-s", "--substitution", None,"lorem ipsum dolor")
parser.add_arg("-e", "--enc-type", None,"lorem ipsum dolor")
parser.add_arg("-x", "--dec", None,"lorem ipsum dolor")
parser.add_arg("-c", "--ciphertext", "ciphertext", description="lorem ipsum dolor")
parser.add_arg("-k", "--key", "key", "lorem ipsum dolor")

if len(sys.argv) == 1 or parser.is_present("-h"):
  # Change to True to add a space between each argument
  parser.show_help(add_space=False)

  # An alternate help screen can also be viewed.
  parser.view_args()

```

Let's run our program.

```shell

$./program.py --help
[+] Usage: ./program.py [options]

[i] Positional arguments:

       -s --substitution
              lorem ipsum dolor
       -e --enc-type
              lorem ipsum dolor
       -x --dec
              lorem ipsum dolor
       -c --ciphertext ciphertext
              lorem ipsum dolor
       -k --key key
              lorem ipsum dolor

[i] Optional arguments:

       -h --help
              Show this help screen and exit.
       -v --version
              Print version information and exit.

```

Similarly, if any comments or examples were
added, they would show up too. Let's keep it
simple for the example, though, so we'll do that
later.

## Error handling

Easyparse should be able to catch these types
of common errors, regardless of whether the long
or short form has been supplied, or different forms
have been mixed:

- Duplicate arguments
- Invalid arguments
- No values passed where required
- Invalid argument type

Let's see a few cases of these.

```shell
$./program -s -s
[!] ./unit_tests.py: Duplicate arguments supplied.

$./program -i
[!] ./unit_tests.py: Option: '-i' missing value

./program -l
[!] ./unit_tests.py: Invalid option: -l
```

## Summary

Let's summarise all the functions we have covered so far:

```Python
# Import the parser
import sys
import easyparse

# initialise an instance of the parser.
# Both the arguments are optional.
parser = easyparse.opt_parser(argument_list=sys.argv, show_colors=True)

# Add an argument
parser.add_arg("-h", "--help", None,"Show this help screen and exit.", optional=True)

# Add a comment
parser.add_comment("Lorem ipsum dolor sit amet.")

# Add an example
parser.add_example("<example>", prepend_name="file-name")

# Once everything is set parse the arguments
parser.parse_args()

# show the help screen
# Both -h and --help can be used
# The help screen will be displayed regardless
# of which form is used.
if len(sys.argv) == 1 or parser.is_present("--help"):
  parser.show_help()

```

## Conclusion

I would like to thank you for taking the time to read
this documentation, I hope someone finds this basic project useful.
If you have any questions at all, please create an issue.

You can view my other projects at my [GitHub page](https://github.com/Sh3llcod3/).

[GitHub Link](https://github.com/sh3llcod3/Easyparse)
