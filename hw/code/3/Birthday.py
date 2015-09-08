import random


# 10.15 Exercise 8


def has_duplicates(input_list):
    input_set = set()
    for input in input_list:
        if input not in input_set:
            input_set.add(input)
        else:
            return True

    return False


def get_random_birthdays():
    birthday_list = []
    for i in range(23):
        birthday_list.append(random.randint(1, 365))

    return birthday_list


def calculate_probability():
    count = 0
    for i in range(1000):
        if has_duplicates(get_random_birthdays()):
            count += 1

    return count/float(1000)
