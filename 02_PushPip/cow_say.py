import argparse
import cowsay

parser = argparse.ArgumentParser(description='Cowsay function')

parser.add_argument("message", nargs='*')
parser.add_argument('-l', action="store_true")
parser.add_argument('-f', type=str, default="default")
parser.add_argument('-e', type=str, default="oo")
parser.add_argument('-T', type=str, default="  ")
parser.add_argument('-W', type=int, default=40)
parser.add_argument('-n', action="store_true")


parser.add_argument('-b', action="store_true")
parser.add_argument('-d', action="store_true")
parser.add_argument('-g', action="store_true")
parser.add_argument('-p', action="store_true")
parser.add_argument('-s', action="store_true")
parser.add_argument('-t', action="store_true")
parser.add_argument('-w', action="store_true")
parser.add_argument('-y', action="store_true")

args = parser.parse_args()


def main():

    if args.l:
        print(cowsay.list_cows())
        return

    wrap_text = True
    if args.n:
        wrap_text = False

    preset = None
    presets = ["b", "d", "g", "p", "s", "t", "w", "y"]

    for p in presets:
        if eval(f"args.{p}"):
            preset = p

    print(cowsay.cowsay(" ".join(args.message),
                        cow=args.f,
                        eyes=args.e,
                        preset=preset,
                        tongue=args.T,
                        width=args.W,
                        wrap_text=wrap_text))


if __name__ == '__main__':
    main()
