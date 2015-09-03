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
def print_line(char1, char2, col_num):
    for i in range(1, col_num+1):
        print char1,
        for j in range(1, 5):
            print char2,
    print char1

def print_grid(**kvargs):
    row_num = kvargs.get('row_num')
    col_num = kvargs.get('col_num')
    f = kvargs.get('func')
    for i in range(1, row_num+1):
        f(kvargs.get('symbol1'), kvargs.get('symbol2'), col_num)
        for j in range(1, 5):
            f(kvargs.get('symbol3'), kvargs.get('symbol4'), col_num)
    f(kvargs.get('symbol1'), kvargs.get('symbol2'), col_num)

print "\n" + "Two Column Grid" + "\n"
print_grid(func=print_line,
           symbol1='+',
           symbol2='-',
           symbol3='|',
           symbol4=' ',
           row_num=2,
           col_num=2)

print "\n" + "Four Column Grid" + "\n"
print_grid(func=print_line,
           symbol1='+',
           symbol2='-',
           symbol3='|',
           symbol4=' ',
           row_num=4,
           col_num=4)