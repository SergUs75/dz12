from classes import AddressBook, Name, Birthday, Phone, Record
import json


address_book = AddressBook()


def input_error(func):
    def wrapper(*args):
        try:
            return func(*args)
        except KeyError:
            return "Contact not found."
        except ValueError:
            return "Invalid input."
        except IndexError:
            return "Invalid command."
        except AttributeError:
            return "Invalid atribut"
    return wrapper


@input_error
def add_command(*args):
    name = Name(args[0])
    rec: Record = address_book.get(str(name))
    if rec:
        phone = Phone(args[1])
        return rec.add_phone(phone)
    birthday = Birthday(args[1])
    phone = Phone(args[2])
    rec = Record(name, birthday, phone)
    return address_book.add_record(rec)


@input_error
def change_command(*args):
    name = Name(args[0])
    old_phone = Phone(args[1])
    new_phone = Phone(args[2])
    rec: Record = address_book.get(str(name))
    if rec:
        return rec.change_phone(old_phone, new_phone)
    return f"No contact {name} in address book"


@input_error
def delete_phone_command(*args):
    name = Name(args[0])
    phone = Phone(args[1])
    rec: Record = address_book.get(str(name))
    if rec:
        return rec.delete_phone(phone)
    return f"No contact {name} in address book"


@input_error
def search_command(*args):
    search = args[0]
    if len(search) > 2:
        return address_book.search(search)
    return f"Not enough characters (at least 3)"

def exit_command(*args):
    return "Bye"


def hello_command():
    return 'How can I help you?'


def unknown_command(*args):
    return 'Unknown command!'


def show_all_command(*args):
    if args:
        result = ''
        page = 1
        for record in address_book.iterator(int(args[0])):
            result += f"page {page}\n" + record
            page += 1
        return result
    else:
        return address_book


COMMANDS = {
    add_command: ("add", "+"),
    change_command: ("change",),
    exit_command: ("bye", "exit", "end"),
    hello_command: ("hello", ),
    show_all_command: ("show all", ),
    delete_phone_command: ("delete phone", ),
    search_command: ("search", )
}


def parser(text:str):
    for cmd, kwds in COMMANDS.items():
        for kwd in kwds:
            if text.lower().startswith(kwd):
                data = text[len(kwd):].strip().split()
                return cmd, data 
    return unknown_command, []


def main():
    address_book.load_json('address_book.json')
    print("Address book data loaded.")

    while True:
        user_input = input(">>>")
        cmd, data = parser(user_input)
        result = cmd(*data)
        print(result)

        if cmd == exit_command:
            address_book.save_json('address_book.json')
            print("The address book data has been saved.")
            break

if __name__ == "__main__":
    main()