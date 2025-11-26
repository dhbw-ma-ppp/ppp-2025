import sys

def say_hello():
    print("Hello, this is your friendly neighbourhoud library...")


if __name__ == '__main__':
    if len(sys.argv) == 1:
        print("you didn't pass any arguments... :(")
        quit()

    # for better option parsing: look at the `argparse` package!
    args = sys.argv[1:]
    if args[0] == '-m' and len(args) > 1:
        print(f'You say: "{args[1]}"')
    else:
        print("Couldn't understand what you want, sorry...") 

    