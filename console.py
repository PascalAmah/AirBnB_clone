#!/usr/bin/python3
import cmd
import models
from models import storage
from models.base_model import BaseModel
from models.user import User


class HBNBCommand(cmd.Cmd):
    """Command interpreter class for HBNB."""
    prompt = "(hbnb) "
    classes = {
            "BaseModel": BaseModel,
            "User": User,
            }

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
        """Usage: show <class> <id> or <class>.show(<id>)
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
        If no class is specified, displays all instantiated objects."""
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

    def do_count(self, arg):
        """Usage: <class>.count()
        Retrieve the number of instances of a given class."""
        args = arg.split()
        if len(args) == 0 or args[0] not in self.classes:
            print("** class doesn't exist **")
        else:
            count = sum(1 for key in models.storage.all()
                        if key.startswith(args[0]))
            print(count)

    def do_update(self, arg):
        """Update an instance of a class by ID.
        Usage: update <class> <id> <attribute_name> <attribute_value
        update <class> <id> <dictionary>"""
        args = arg.split(" ", 2)
        if not args:
            print("** class name missing **")
        if len(args) < 2:
            print("** instance id missing **")
            return
        if args[0] not in self.classes:
            print("** class doesn't exist **")
            return
        key = f"{args[0]}.{args[1]}"
        obj = models.storage.all().get(key)
        if obj is None:
            print("** no instance found **")
            return
        if len(args) == 2:
            print("** attribute name missing **")
            return
        if args[2].startswith("{") and args[2].endswith("}"):
            try:
                updates = eval(args[2])
                if isinstance(updates, dict):
                    for attr, val in updates.items():
                        setattr(obj, attr, type(getattr(obj, attr, val))(val))
                        obj.save()
            except Exception:
                print("** invalid dictionary format **")
            return
        try:
            attr, val = args[2].split(" ", 1)
            setattr(obj, attr, type(getattr(obj, attr, val))(val.strip("\"'")))
            obj.save()
        except ValueError:
            print("** invalid value type **")

    def default(self, line):
        """Handle commands in the format <class>.<command>(<args>)."""
        args = line.split(".")
        if len(args) != 2:
            print(f"*** Unknown syntax: {line}")
            return

        class_name, command = args[0], args[1]
        if class_name not in self.classes:
            print(f"*** Unknown syntax: {line}")
            return

        if "(" in command and command.endswith(")"):
            command_name, params = command[:-1].split("(", 1)
            params = params.strip("\"")
            argdict = {
                    "all": self.do_all,
                    "show": self.do_show,
                    "destroy": self.do_destroy,
                    "update": self.do_update,
                    "count": self.do_count,
                    }
            if command_name in argdict:
                full_args = f"{class_name} {params}" if params else class_name
                argdict[command_name](full_args)
            else:
                print(f"*** Unknown syntax: {line}")
        else:
            print(f"*** Unknown syntax: {line}")


if __name__ == "__main__":
    HBNBCommand().cmdloop()
