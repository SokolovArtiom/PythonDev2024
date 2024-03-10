import cmd
import shlex
import cowsay

EYES = ["uu", "$$", "XX"]
TONGUES = ["U", "T", "W"]


class cowsay_cmd(cmd.Cmd):
    prompt = "cmd>> "

    def do_list_cows(self, arg):
        """
        Returns list of possible cows
        """
        print(cowsay.list_cows())

    def do_cowsay(self, arg):
        """
        Parameters are listed with their
        corresponding options in the cowsay command. Returns the resulting cowsay
        string

        :param message: The message to be displayed
        :param cow: -f – the available cows can be found by calling list_cows
        :param eyes: -e or eye_string
        :param tongue: -T or tongue_string
        """

        commands = shlex.split(arg)

        message = commands[0]

        if "-e" in commands:
            eye = commands[commands.index("-e") + 1]
        else:
            eye = 'oo'

        if "-f" in commands:
            cow = commands[commands.index("-f") + 1]
        else:
            cow = "default"

        if "-T" in commands:
            tongue = commands[commands.index("-T") + 1]
        else:
            tongue = "  "

        print(cowsay.cowsay(message,
                            cow=cow,
                            eyes=eye,
                            tongue=tongue))

    def do_cowthink(self, arg):
        """
        Parameters are listed with their
        corresponding options in the cowthink command. Returns the resulting
        cowthink string

        :param message: The message to be displayed
        :param cow: -f – the available cows can be found by calling list_cows
        :param eyes: -e or eye_string
        :param tongue: -T or tongue_string
        """

        commands = shlex.split(arg)

        message = commands[0]

        if "-e" in commands:
            eye = commands[commands.index("-e") + 1]
        else:
            eye = 'oo'

        if "-f" in commands:
            cow = commands[commands.index("-f") + 1]
        else:
            cow = "default"

        if "-T" in commands:
            tongue = commands[commands.index("-T") + 1]
        else:
            tongue = "  "

        print(cowsay.cowthink(message,
                              cow=cow,
                              eyes=eye,
                              tongue=tongue))

    def do_make_bubble(self, arg):
        """
        Wraps text is wrap_text is true, then pads text and sets inside a bubble.
        This is the text that appears above the cows
        """

        commands = shlex.split(arg)

        message = commands[0]

        if "-n" in commands:
            wrap_text = False
            print("+")
        else:
            wrap_text = True

        if "-W" in commands:
            W = int(commands[commands.index("-W") + 1])
        else:
            W = 40

        print(cowsay.make_bubble(message,
                                 wrap_text=wrap_text,
                                 width=W))

    def complete_cowsay(self, text, line, begidx, endidx):

        words = shlex.split(line[:endidx])

        if words[-1] == "-e":
            return EYES
        elif words[-1] == "-T":
            return TONGUES
        elif words[-1] == "-f":
            return cowsay.list_cows()

    def complete_cowthink(self, text, line, begidx, endidx):

        words = shlex.split(line[:endidx])

        if words[-1] == "-e":
            return EYES
        elif words[-1] == "-T":
            return TONGUES
        elif words[-1] == "-f":
            return cowsay.list_cows()


if __name__ == '__main__':
    cowsay_cmd().cmdloop()
