import cmd
import threading
import readline
import shlex
import socket
import sys
import select

s = None
client_flag = True
compl_msg = None
HOST = '0.0.0.0'
PORT = 1337


def write(msg):
    s.send(f"{msg}\n".encode())


def recieve(cmdline):
    global compl_msg

    while client_flag:
        data = s.recv(1024).decode().strip()
        data = data.split("@")
        if data and len(data) == 1:
            print(f'\n{data[0]}\n{cmdline.prompt}{readline.get_line_buffer()}', end="", flush=True)
        elif data and data[0].strip() == "compl":
            compl_msg = data[1]


class cowsay_cmd(cmd.Cmd):
    prompt = "cmd>> "

    def do_who(self, arg):
        """
        who
        Lists all registred users
        """
        write("who")

    def do_cows(self, arg):
        """
        cows
        Lists all free cows
        """

        write("cows")

    def do_login(self, arg):
        """
        login usr_login
        Registers with <usr_login> name
        """

        write(f"login {arg}")

    def complete_login(self, text, line, begidx, endidx):

        global compl_msg

        write(f"compl@cows")
        while compl_msg is None:
            pass

        data = compl_msg[1:-1].replace("'", "").split(",")
        compl_msg = None

        data = list(map(lambda x: x.strip(), data))

        if line.split()[-1] == "login":
            return data
        else:
            return [s for s in data if s.startswith(line.split()[-1])]

    def do_say(self, arg):
        """
        say usr msg
        Sends <msg> to <usr>
        """
        cow, msg = shlex.split(arg)
        write(f"say {cow} {msg}")

    def complete_say(self, text, line, begidx, endidx):

        global compl_msg

        write(f"compl@who")
        while compl_msg is None:
            pass

        data = compl_msg[1:-1].replace("'", "").split(",")
        compl_msg = None

        data = list(map(lambda x: x.strip(), data))

        if line.split()[-1] == "say":
            return data
        else:
            return [s for s in data if s.startswith(line.split()[-1])]

    def do_yield(self, arg):
        """
        yield msg
        sends <msg> to all users
        """
        write(f"yield {arg}")

    def do_quit(self, args):
        """
        quit
        logout usr
        """
        write("quit")


if __name__ == "__main__":

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, int(PORT)))

    cmdline = cowsay_cmd()
    thread = threading.Thread(target=recieve, args=(cmdline, ))
    thread.start()
    cmdline.cmdloop()

    s.close()
    client_flag = False
