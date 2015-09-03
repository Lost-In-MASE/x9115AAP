#Exercise 3.1 and 3.2
def repeat_lyrics():
    print_lyrics()
    print_lyrics()


def print_lyrics():
    print "I'm a lumberjack, and I'm okay."
    print "I sleep all night and I work all day."

repeat_lyrics()

#Exercise 3.3
def right_justify(string1):
    print "%70s" %string1

right_justify("allen")

#Exercise 3.4
def do_twice(f, val):
    f(val)
    f(val)

def do_four(f, val):
    do_twice(f, val)
    do_twice(f, val)

def print_twice(val):
    print val

def print_spam():
    print 'spam'

do_twice(print_twice, "spam")
do_four(print_twice, "spam")

#Exercise 3.5
def print_line(char1, char2):
    print char1,
    for i in range(1, 5):
        print char2,
    print char1,
    for i in range(1, 5):
        print char2,
    print char1

def print_grid(f, char1, char2, char3, char4):
    f(char1, char2)
    for i in range(1, 5):
        f(char3, char4)
    f(char1, char2)
    for i in range(1, 5):
        f(char3, char4)
    f(char1, char2)


print_grid(print_line, '+', '-', '|', ' ')