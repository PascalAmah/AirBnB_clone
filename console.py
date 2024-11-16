#!/usr/bin/python3
import cmd


class HBNBCommand(cmd.Cmd):
    """Command interpreter class for HBNB."""
    prompt = "(hbnb) "

    def do_quit(self, arg):
        """Quit command to exit the program."""
        return True

    def do_EOF(self, arg):
        """Exit the program using EOF signal."""
        print()
        return True

    def emptyline(self):
        """Do nothing upon receiving an empty line."""
        pass


if __name__ == "__main__":
    HBNBCommand().cmdloop()
