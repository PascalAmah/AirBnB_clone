#!/usr/bin/python3
import cmd
import models
from models.base_model import BaseModel


class HBNBCommand(cmd.Cmd):
    """Command interpreter class for HBNB."""
    prompt = "(hbnb) "
    classes = {"BaseModel": BaseModel}

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

    def do_create(self, arg):
        """Usage: create <class>
        Create a new class instance, save it
        and print its id"""
        args = arg.split()
        if len(args) == 0:
            print("** class name missing **")
        elif args[0] not in self.classes:
            print("** class doesn't exist **")
        else:
            obj = self.classes[args[0]]()
            obj.save()
            print(obj.id)

    def do_show(self, arg):
        """Usage: show <class> <id> or <class>.shoe(<id>)
        Display the string representation of a class instance of a given id.
        """
        args = arg.split()
        if len(args) == 0:
            print("** class name missing **")
        elif args[0] not in self.classes:
            print("** class doesn't exist **")
        elif len(args) == 1:
            print("** instance id missing **")
        else:
            key = f"{args[0]}.{args[1]}"
            obj = models.storage.all().get(key)
            if obj is None:
                print("** no instance found **")
            else:
                print(obj)

    def do_destroy(self, arg):
        """Usage: destroy <class> <id> or <class>.destroy(<id>)
        Delete an instance by class name and id."""
        args = arg.split()
        if len(args) == 0:
            print("** class name missing **")
        elif args[0] not in self.classes:
            print("** class doesn't exist **")
        elif len(args) == 1:
            print("** instance id missing **")
        else:
            key = f"{args[0]}.{args[1]}"
            if key in models.storage.all():
                del models.storage.all()[key]
                models.storage.save()
            else:
                print("** no instance found **")

    def do_all(self, arg):
        """Usage: all or all <class> or <class>.all()
        Display string representations of all instances of a given class.
        If no class is specifired, displays all instantiated objects."""
        args = arg.split()
        obj_list = []
        if len(args) == 0:
            obj_list = [str(obj) for obj in models.storage.all().values()]
        elif args[0] in self.classes:
            obj_list = [
                str(obj) for key, obj in models.storage.all().items()
                if key.startswith(args[0])
            ]
        else:
            print("** class doesn't exist **")
            return
        print(obj_list)

    def do_update(self, arg):
        """Usage: update <class> <id> <attribute_name> <attribute_value> or
        <class>.update(<id>, <attribute_name>, <attribute_value>) or
        <class>.update(<id>, <dictionary>)
        Update an instance based on class name and id."""
        args = arg.split()
        if len(args) == 0:
            print("** class name missing **")
        elif args[0] not in self.classes:
            print("** class doesn't exist **")
        elif len(args) == 1:
            print("** instance id missing **")
        else:
            key = f"{args[0]}.{args[1]}"
            obj = models.storage.all().get(key)
            if obj is None:
                print("** no instance found **")
            elif len(args) == 2:
                print("** attribute name missing **")
            elif len(args) == 3:
                print("** value missing **")
            else:
                attr_name = args[2]
                attr_value = args[3].strip('"')
                try:
                    if "." in attr_value:
                        attr_value = float(attr_value)
                    else:
                        attr_value = int(attr_value)
                except ValueError:
                    pass
                setattr(obj, attr_name, attr_value)
                obj.save()


if __name__ == "__main__":
    HBNBCommand().cmdloop()
