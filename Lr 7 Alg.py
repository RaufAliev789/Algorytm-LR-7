class PhoneBook:
    def __init__(self):
        self.entries = {}  # Для хранения (номер, имя)
        self.name_to_numbers = {}  # Для поиска по имени
        self.history = []  # История операций для undo

    def add(self, number, name):
        # Сохраняем текущее состояние для возможности отмены
        if number in self.entries:
            old_name = self.entries[number]
            self.history.append(('add', number, old_name))  # Если обновление, сохраняем старое имя
        else:
            self.history.append(('add', number, None))  # Новый контакт, старого имени нет

        self.entries[number] = name

        # Обновляем обратный индекс для поиска по именам
        if name not in self.name_to_numbers:
            self.name_to_numbers[name] = set()
        self.name_to_numbers[name].add(number)

    def del_entry(self, number):
        if number in self.entries:
            name = self.entries[number]
            self.history.append(('del', number, name))  # Сохраняем полное состояние для undo
            del self.entries[number]

            # Удаляем номер из обратного индекса
            if name in self.name_to_numbers:
                self.name_to_numbers[name].remove(number)
                if not self.name_to_numbers[name]:
                    del self.name_to_numbers[name]

    def find_by_number(self, number):
        return self.entries.get(number, "not found")

    def find_by_name(self, name):
        return self.name_to_numbers.get(name, set())

    def undo(self):
        if not self.history:
            return

        last_operation = self.history.pop()
        op_type, number, name = last_operation

        if op_type == 'add':
            if name is not None:
                # Восстановление старого имени
                self.entries[number] = name
                if name not in self.name_to_numbers:
                    self.name_to_numbers[name] = set()
                self.name_to_numbers[name].add(number)
            else:
                # Если это был новый контакт, удаляем его
                del self.entries[number]
                for key in list(self.name_to_numbers.keys()):
                    if number in self.name_to_numbers[key]:
                        self.name_to_numbers[key].remove(number)
                        if not self.name_to_numbers[key]:
                            del self.name_to_numbers[key]
        elif op_type == 'del':
            # Восстановление удалённого контакта
            self.entries[number] = name
            if name not in self.name_to_numbers:
                self.name_to_numbers[name] = set()
            self.name_to_numbers[name].add(number)


# Пример использования
phone_book = PhoneBook()

n = int(input("Введите число запросов: "))  # Число запросов
for _ in range(n):
    command = input().strip().split(maxsplit=2)
    if command[0] == "add":
        number = command[1]
        name = command[2]
        phone_book.add(number, name)
    elif command[0] == "del":
        number = command[1]
        phone_book.del_entry(number)
    elif command[0] == "find":
        number = command[1]
        print(phone_book.find_by_number(number))
    elif command[0] == "find_name":
        name = command[1]
        numbers = phone_book.find_by_name(name)
        if numbers:
            print(" ".join(numbers))
        else:
            print("not found")
    elif command[0] == "undo":
        phone_book.undo()
