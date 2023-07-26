from collections import UserDict
from datetime import date, datetime
import json


class Field:
    
    def __init__(self, value) -> None:
        self.__value = None
        self.value = value

    def __eq__(self, other):
        if isinstance(other, Field):
            return self.value == other.value
    
    def __str__(self) -> str:
        return self.value
    
    def __repr__(self) -> str:
        return str(self)
        

class Name(Field):
    ...
    

class Phone(Field):
    
    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value: str):
        if value:
            value = value.removeprefix("+")
            if len(value) != 12 or not value.isdigit():
                try:
                    raise ValueError(f"Invalid phone format in {value}. Please use +XXXXXXXXXXXX format.")
                except ValueError as e:
                    print(f"ValueError: {e}")
            else:
                value = f"+{value}"       
                self.__value = value 

    def __str__(self):
        return f"{self.value}"


class Birthday(Field):
    
    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value:str):
        if value:
            try:
                day, month, year = map(int, value.split('.'))
                date(year, month, day)
                self.__value = date(year, month, day)              
            except ValueError:
                 raise ValueError("Invalid birthday format. Please use dd.mm.YYYY format.")
            
    def __str__(self) -> str:
        return self.value.strftime("%d.%m.%Y")


class Record:
    
    def __init__(self, name: Name, birthday: Birthday = None, phone: Phone = None) -> None:
        self.name = name
        self.birthday = birthday
        self.phones = []
        if phone:
            self.phones.append(phone)
    
    def add_phone(self, phone: Phone):
        if phone.value not in [p.value for p in self.phones]:
            self.phones.append(phone)
            return f"phone {phone} add to contact {self.name}"
        return f"{phone} present in phones of contact {self.name}"
    
    def change_phone(self, old_phone, new_phone):
        for idx, p in enumerate(self.phones):
            if old_phone.value == p.value:
                self.phones[idx] = new_phone
                return f"old phone {old_phone} change to {new_phone}"
        return f"{old_phone} not present in phones of contact {self.name}"
    
    def delete_phone(self, phone: Phone):
        for p in self.phones:
            if phone.value == p.value:
                self.phones.remove(p)
                return f"Phone {phone} deleted from contact {self.name}."
        return f"Phone {phone} not found in contact {self.name}."
    
    def __str__(self) -> str:
        return f"{self.name} {str(self.birthday)} ({self.days_to_birthday(self.birthday)}): {', '.join(str(p) for p in self.phones)}"

    def days_to_birthday(self, birthday: Birthday) -> int:
        if self.birthday:
            day = self.birthday.value.day
            month = self.birthday.value.month
            today = date.today()
            try:
                birthday = date(today.year, month, day)
            except ValueError:
                birthday = date(today.year, 3, 1)
            if birthday < today:
                try:
                    birthday = date(today.year + 1, month, day)
                except ValueError:
                    birthday = date(today.year + 1, 3, 1)
            delta = (birthday - today).days    
            return delta
        else:
            return None


class AddressBook(UserDict):

    def add_record(self, record: Record):
        self.data[str(record.name)] = record
        return f"Contact {record} add success"

    def __str__(self) -> str:
        return "\n".join(str(r) for r in self.data.values())

    def iterator(self, n):
        count = 0
        page = ""
        for record in self.data.values():
            page += (str(record)) + "\n"
            count += 1
            if count >= n:
                yield page
                count = 0
                page = ""
        if page:
            yield page
            
      
    def search(self, search: str) -> list:
        result = []
        for record in self.data.values():
            if search in str(record):
                result.append(record)
        return "\n".join(str(r) for r in result)


    def save_json(self, file_path):
        with open(file_path, 'w') as file:
            json_data = []
            for record in self.data.values():
                json_data.append({
                    'name': record.name.value,
                    'birthday': str(record.birthday.value.strftime("%d.%m.%Y")),
                    'phones': [phone.value for phone in record.phones]
                })
            json.dump(json_data, file)

    
    def load_json(self, file_path):
        try:
            with open(file_path, 'r') as file:
                    data = json.load(file)
                    for value in data:
                        name = Name(value['name'])
                        birthday = Birthday(value['birthday'])
                        phones = [Phone(phone) for phone in value['phones']]
                        record = Record(name, birthday, *phones)
                        self.data[str(record.name)] = record
        except (FileNotFoundError, json.JSONDecodeError):
            print(f"The file {file_path} is missing or does not contain valid JSON data.")