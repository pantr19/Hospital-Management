from colorama import init
import pyfiglet
import os
from variables import Docs, Var
from termcolor import colored
from random import randint
from datetime import datetime, date
init()


# start miscellaneous functions {
def Cscreen():
    os.system('cls')
    os.system('cls')


def docs_printer(which):
    data = {
            1: Docs.Greeter,
            2: Docs.Authentication,
            3: Docs.Home,
            4: Docs.Entry,
            5: Docs.Read_Update,
            6: Docs.Admin
            }
    print(
        colored(
            data.get(which), "green", attrs=["bold"]
        )
    )


def Greeter(text):
    """ function to greet user with Figlet and print documentation"""
    text = text.split()
    font_list = [
                'univers', 'starwars',
                'smisome1', 'roman',
                'puffy', 'nancyj',
                'larry3d', 'isometric4',
                'epic', 'dotmatrix'
                ]

    font = font_list[randint(0, len(font_list) - 1)]
    figlet = pyfiglet.Figlet(font=font, width=200)
    for I in text:
        print(
            colored(
                figlet.renderText(I), "yellow", attrs=["bold"]
            )
        )


def Time():
    """ function to obtain time"""
    now = datetime.now()
    current_time = now.strftime("%H:%M")
    return current_time


def Date():
    """ function to obtain date"""
    now = str(date.today())
    return now


def Sprint(text, space_less=False):
    """ function to print a text specially"""
    if space_less is True:
        print(colored(text, "yellow", attrs=["bold"]))
        print("\n")
    else:
        print("\n")
        print(colored(text, "yellow", attrs=["bold"]))
        print("\n")


def Qmark(status, symbol):
    """ operation to create qmark"""

    if status is not None:
        username, mode = status
        now = Time()
        prompt = "?({})@{}::{}~[{}]>".format(now, username, mode, symbol)

    else:
        now = Time()
        prompt = "?({})~[{}]>".format(now, symbol)

    return prompt


def Cprint(statement, status):
    """ function to print on console"""
    username, mode = status
    now = Time()
    print(
        colored("$({})@{}::{}>".format(now, username, mode), "yellow", attrs=["bold"]),
        colored(statement, "white", attrs=["bold"]))


def Tprint(table):
    """ function to print tables"""
    print(
        colored(
            table, "white", attrs=["bold"]
        )
    )


def Wprint(warning):
    """ function to print warnings"""
    print(
        colored(
            warning, "red", attrs=["bold"])
    )


def Qprint(field, value):
    """ function to print user entered values before entering into table"""
    print(colored("$", "white", attrs=["bold"]),
          colored("value entered by the user for -->", "white", attrs=["bold"]),
          colored(field, "yellow", attrs=["bold"]),
          colored(" : ", "white", attrs=["bold"]),
          colored(str(value), "magenta", attrs=["bold"])
          )


def UQprint(field, value):
    """ function to print user entered values before entering into table"""
    old, new = value
    print(colored("$", "white", attrs=["bold"]),
          colored("value entered by the user for -->", "white", attrs=["bold"]),
          colored("[old value - new value]", "blue", attrs=["bold"]),
          colored(field, "yellow", attrs=["bold"]),
          colored(" : ", "white", attrs=["bold"]),
          colored(str(old), "magenta", attrs=["bold"]),
          colored(" ---> ", "white", attrs=["bold"]),
          colored(str(new), "magenta", attrs=["bold"])
          )


def Dcheck(data):
    """ function to check and convert user entered date to datetime.date"""
    try:
        argument = data.split("-")
        year = int(argument[0])
        month = int(argument[1])
        day = int(argument[2])
        datetime(year, month, day)
        now = date(year, month, day)
        return [True, now]
    except:
        return [False]


def Check(data):
    properties = Var.pfields
    all_keys = properties.keys()
    integrity = True
    checked_data = {}
    error_keys = []
    error = None
    for a in data.items():

        if a[0] in all_keys:
            if a[1] == "N/A":
                checked_data[a[0]] = None

            elif properties[a[0]] == "str":
                if a[1] is not None:
                    try:
                        checked_data[a[0]] = str(a[1])
                    except:
                        error_keys.append(a[0])
                else:
                    checked_data[a[0]] = None

            elif properties[a[0]] == "int":
                if a[1] is not None:
                    try:
                        checked_data[a[0]] = int(a[1])
                    except:
                        error_keys.append(a[0])
                else:
                    checked_data[a[0]] = None

            elif properties[a[0]] == "sex":
                if a[1] not in ["Male", "Female"]:
                    error_keys.append(a[0])
                else:
                    checked_data[a[0]] = a[1]

            elif properties[a[0]] == "float":
                if a[1] is not None:
                    try:
                        checked_data[a[0]] = float(a[1])
                    except:
                        error_keys.append(a[0])
                else:
                    checked_data[a[0]] = None

            elif properties[a[0]] == "Date":
                if a[1] is not None:
                    date = Dcheck(a[1])
                    if date[0] is True:
                        checked_data[a[0]] = date[1]
                    else:
                        error_keys.append(a[0])
                else:
                    checked_data[a[0]] = None

    if len(error_keys) != 0:
        integrity = False
        error = "There is an error with fields : {}".format(error_keys)
    return integrity, checked_data, error
#   } end miscellaneous functions
