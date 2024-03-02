import argparse
import random
from cowsay import cowsay, list_cows
import urllib.robotparser

parser = argparse.ArgumentParser(description='Cowsay function')

parser.add_argument("inp", type=str, nargs="*")

args = parser.parse_args()

cow_list = list_cows()


def bullscows(guess: str, secret: str) -> (int, int):

    if len(guess) != len(secret):
        assert "Word's length is incorrect"

    oxens = 0
    g_d = {}
    s_d = {}
    for i in range(len(guess)):

        cur_g = guess[i]
        cur_s = secret[i]

        if cur_g == cur_s:
            oxens += 1

        if cur_g not in g_d:
            g_d[cur_g] = 1
        else:
            g_d[cur_g] += 1

        if cur_s not in s_d:
            s_d[cur_s] = 1
        else:
            s_d[cur_s] += 1

    cows = 0
    for l in s_d:
        if l in g_d:
            cows += min(s_d[l], g_d[l])

    cows -= oxens

    return oxens, cows


def ask(prompt: str, valid: list[str] = None) -> str:

    while True:

        print(cowsay(prompt,
                     cow=random.choice(cow_list)))

        inp = input()

        if valid is not None and inp not in valid:
            pass
        else:
            return inp


def inform(format_string: str, bulls: int, cows: int) -> None:

    print(cowsay(format_string.format(bulls, cows),
                 cow=random.choice(cow_list)))


def gameplay(ask: callable, inform: callable, words: list[str]) -> int:

    secret = random.choice(words)

    tries = 0

    while True:

        guess = ask("Введите слово: ", words)
        tries += 1
        oxens, cows = bullscows(guess, secret)
        inform("Быки: {}, Коровы: {}", oxens, cows)

        if oxens == len(secret):
            break

    return tries


def main():

    file = args.inp[0]
    if len(args.inp) == 1:
        l = 5
    elif len(args.inp) == 2:
        l = args.inp[1]

    if file[:6] == "https:":
        words = urllib.request.urlopen(file).readlines()
        words = list(map(lambda x: x.decode("utf-8")[:-1], words))
    else:
        with open(file, "r") as f:
            words = f.readlines()
            words = list(map(lambda x: x[:-1], words))

    words = list(filter(lambda x: len(x) == int(l), words))

    n_tries = gameplay(ask, inform, words)

    print(f"Игра окончена. Попыток сделано: {n_tries}")


if __name__ == '__main__':
    main()
