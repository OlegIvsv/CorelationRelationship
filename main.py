from math_helpers import MathHelperSmall, MathHelperLarge
import re

##-----##-----##-----##-----##-----##-----##

DEFAULT_LARGE_DATA_X = "0.32 0.34 0.34 0.49 0.52 0.81 0.88 0.57 0.42 0.25 0.86 0.99 0.72 0.43 0.25 0.78\
 0.29 0.35 0.34 0.42 0.47 0.60 0.34 0.49 0.91 0.24 0.32 0.34 0.41 0.57 0.86 0.99"
DEFAULT_LARGE_DATA_Y = "0.29 0.31 0.65 0.76 0.43 0.32 0.10 0.00 0.34 0.10 0.00 0.02 0.22 0.29 0.31 0.43\
 0.24 0.32 0.35 0.43 0.62 0.81 0.43 0.27 0.99 0.59 0.43 0.23 0.12 0.24 0.65 0.76"
DEFAULT_SMALL_DATA_X = "0.32 0.34 0.34 0.49 0.52 0.81 0.88 0.57 0.42 0.25 0.86 0.99 0.72 0.43 0.25 0.78"
DEFAULT_SMALL_DATA_Y = "0.29 0.31 0.65 0.76 0.43 0.32 0.10 0.00 0.34 0.10 0.00 0.02 0.22 0.29 0.31 0.43"


def main():
    mode = read_mode()
    executor = for_large_data if mode else for_small_data

    data_x = read_array("Enter X : ", DEFAULT_LARGE_DATA_X if mode else DEFAULT_SMALL_DATA_X)
    data_y = read_array("Enter Y : ", DEFAULT_LARGE_DATA_Y if mode else DEFAULT_SMALL_DATA_Y)

    executor(data_x, data_y)


def for_large_data(data_x, data_y):
    calculator = MathHelperLarge()
    calculator.data_x = data_x
    calculator.data_y = data_y
    calculator.print_calculation()


def for_small_data(data_x, data_y):
    calculator_small = MathHelperSmall()
    calculator_small.data_x = data_x
    calculator_small.data_y = data_y
    alpha = read_alpha()
    calculator_small.print_calculation(alpha)


def read_array(request, default_value):
    elements = None;
    try:
        parts = getElemsFromStr(input(request))
        elements = [float(elem) for elem in parts]
    except:
        is_valid_reply = False
        while not is_valid_reply:

            is_valid_reply = True
            reply = input("Incorrect input! Use default value? [Y / N] : ")

            if reply.upper() == "Y":
                parts = default_value.split(" ")
                parts = [x.strip() for x in parts if not x.isspace() or x == ""]
                elements = [float(elem) for elem in parts]
            elif reply.upper() == "N":
                return []
            else:
                is_valid_reply = False

    return elements


def read_alpha():
    is_valid = False;

    while not is_valid:

        precision = 0
        try:
            precision = float(input("Alpha : ").replace(",", "."))
        except:
            pass

        if 1 > precision > 0:
            is_valid = True
        else:
            print("Incorrect input!!!")

    return precision


def read_mode():
    got = False
    while not got:
        answer = (input("[Small / Large] data : ")).lower()
        if answer == "small":
            return False
        elif answer == "large":
            return True


def getElemsFromStr(str):
    list_of_read = re.split(";|s", str.replace(",", "."))
    elems = [float(el.strip()) for el in list_of_read]
    return elems


##-----##-----##-----##-----##-----##-----##

main()
