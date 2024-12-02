import datetime
import json
import csv



class Note:
    def __init__(self, note_id, title, content, timestamp):
        self.note_id = note_id
        self.title = title
        self.content = content
        self.timestamp = timestamp

    def to_dict(self):
        return {
            'note_id': self.note_id,
            'title': self.title,
            'content': self.content,
            'timestamp': self.timestamp
        }

class NoteManager:
    def __init__(self):
        self.note_list = []
        self.load_notes()

    def find_note(self, note_id):
        for note in self.note_list:
            if note.note_id == note_id:
                return note
        return None

    def view_note(self, note_id):
        note = self.find_note(note_id)
        if note:
            print(f'ID: {note.note_id}\nЗаголовок: {note.title}\nСодержание: {note.content}\nВремя создания: {note.timestamp}')
        else:
            print(f'Заметка с ID {note_id} не найдена...')

    def list_notes(self):
        if self.note_list:
            for note in self.note_list:
                print(self.view_note(note.note_id))
        else:
            print('Список заметок пуст...')

    def add_note(self, title, content):
        timestamp = datetime.datetime.now().strftime('%d-%m-%Y %H:%M:%S')
        max_id = max((note.note_id for note in self.note_list), default=0) + 1
        new_note = Note(max_id, title, content, timestamp)
        self.note_list.append(new_note)
        self.save_notes()
        print('Заметка добавлена!')

    def save_notes(self):
        notes_dicts = [note.to_dict() for note in self.note_list]
        with open('notes.json', 'w') as file:
            json.dump(notes_dicts, file, indent=4)

    def load_notes(self):
        try:
            with open('notes.json', 'r') as file:
                notes = json.load(file)
            self.note_list = [Note(**note) for note in notes]
        except FileNotFoundError:
            print('Нет сохранённых заметок')

    def delete_note(self, note_id):
        note = self.find_note(note_id)
        if note:
            self.note_list.remove(note)
            self.save_notes()
            print('Заметка удалена')
        else:
            print('Заметка не найдена')

    def edit_note(self, note_id, edit_dict):
        note = self.find_note(note_id)
        if note:
            for key, value in edit_dict.items():
                if key == 'title':
                    note.title = value
                elif key == 'content':
                    note.content = value
            note.timestamp = datetime.datetime.now().strftime('%d-%m-%Y %H:%M:%S')
            self.save_notes()
            print('Изменения внесены!')
        else:
            print('Заметка не найдена')

    def export_csv(self, filename):
        notes_dicts = [note.to_dict() for note in self.note_list]
        with open(filename, 'w', newline='') as file:
            dict_writer = csv.DictWriter(file, fieldnames=['note_id', 'title', 'content', 'timestamp'])
            dict_writer.writeheader()
            dict_writer.writerows(notes_dicts)
        print('Данные успешно экспортированы')

    def import_csv(self, filename):
        try:
            with open(filename, 'r', newline='') as file:
                dict_reader = csv.DictReader(file)
                for row in dict_reader:
                    self.note_list.append(Note(**row))
            self.save_notes()
            print('Данные успешно импортированы')
        except FileNotFoundError:
            print('Файл не найден...')




class Task:
    def __init__(self, task_id, title, description, priority, due_date):
        self.task_id = task_id
        self.title = title
        self.description = description
        self.priority = priority
        self.due_date = due_date
        self.done = False

    def to_dict(self):
        return {
            'task_id': self.task_id,
            'title': self.title,
            'description': self.description,
            'done': self.done,
            'priority': self.priority,
            'due_date': self.due_date
        }


class TaskManager:
    def __init__(self):
        self.task_list = []
        self.load_tasks()

    def find_task(self, task_id):
        for task in self.task_list:
            if task.task_id == task_id:
                return task
        return None

    def view_task(self, task_id):
        task = self.find_task(task_id)
        if task:
            status = 'Выполнена' if task.done else 'Не выполнена'
            print(
                f'ID: {task.task_id}'
                f'\nКраткое описание: {task.title}'
                f'\nСтатус: {status}'
                f'\nПриоритет: {task.priority}',
                f'\nСрок: {task.due_date}'
            )
        else:
            print(f'Задача с ID {task_id} не найдена...')

    def show_list_tasks(self, status=None, priority=None, due_date=None):
        filtered_tasks = self.task_list

        if status is not None:
            filtered_tasks = [task for task in filtered_tasks if task.done == status]

        if priority is not None:
            filtered_tasks = [task for task in filtered_tasks if task.priority == priority]

        if due_date is not None:
            due_date = datetime.datetime.strptime(due_date, '%d-%m-%Y')
            filtered_tasks = [task for task in filtered_tasks if task.due_date <= due_date]

        for task in filtered_tasks:
            print(task)

    def add_task(self, title, description, priority, due_date):
        date = datetime.datetime.strptime(due_date, '%d-%m-%Y')
        max_id = max((task.task_id for task in self.task_list), default=0) + 1
        new_task = Task(max_id, title, description, priority, date)
        self.task_list.append(new_task)
        self.save_tasks()
        print('Задача добавлена!')

    def save_tasks(self):
        tasks_dicts = [task.to_dict() for task in self.task_list]
        with open('tasks.json', 'w') as file:
            json.dump(tasks_dicts, file, indent=4)

    def load_tasks(self):
        try:
            with open('tasks.json', 'r') as file:
                tasks = json.load(file)
            self.task_list = [Task(**task) for task in tasks]
        except FileNotFoundError:
            print('Нет сохранённых задач')

    def delete_task(self, task_id):
        task = self.find_task(task_id)
        if task:
            self.task_list.remove(task)
            self.save_tasks()
            print('Задача удалена')
        else:
            print('Задача не найдена')

    def edit_task(self, task_id, edit_dict):
        task = self.find_task(task_id)
        if task:
            for key, value in edit_dict.items():
                if key == 'title':
                    task.title = value
                elif key == 'description':
                    task.description = value
                elif key == 'priority':
                    task.priority = value
                elif key == 'due_date':
                    task.due_date = datetime.datetime.strptime(value, '%d-%m-%Y')
            self.save_tasks()
            print('Изменения внесены!')
        else:
            print('Задача не найдена')

    def change_done(self, task_id):
        task = self.find_task(task_id)
        if task:
            task.done = True
        else:
            print('Задача не найдена...')


    def export_csv(self, filename):
        tasks_dicts = [task.to_dict() for task in self.task_list]
        with open(filename, 'w', newline='') as file:
            dict_writer = csv.DictWriter(file, fieldnames=['task_id', 'title', 'description', 'done', 'priority', 'due_date'])
            dict_writer.writeheader()
            dict_writer.writerows(tasks_dicts)
        print('Данные успешно экспортированы')

    def import_csv(self, filename):
        try:
            with open(filename, 'r', newline='') as file:
                dict_reader = csv.DictReader(file)
                for task in dict_reader:
                    self.task_list.append(Contact(**task))
            self.save_tasks()
            print('Данные успешно импортированы')
        except FileNotFoundError:
            print('Файл не найден...')





class Contact:
    def __init__(self, contact_id, name, phone, email):
        self.contact_id = contact_id
        self.name = name
        self.phone = phone
        self.email = email

    def to_dict(self):
        return {
            'contact_id': self.contact_id,
            'name': self.name,
            'phone': self.phone,
            'email': self.email,
        }


class ContactManager:
    def __init__(self):
        self.contact_list = []
        self.load_contacts()

    def find_contact(self, info):
        for contact in self.contact_list:
            if contact.name == info or contact.phone == info:
                return contact
        return None

    def add_contact(self, name, phone, email):
        max_id = max((contact.contact_id for contact in self.contact_list), default=0) + 1
        new_contact = Contact(max_id, name, phone, email)
        self.contact_list.append(new_contact)
        self.save_contacts()
        print('Контакт добавлен!')

    def save_contacts(self):
        contacts_dicts = [contact.to_dict() for contact in self.contact_list]
        with open('contacts.json', 'w') as file:
            json.dump(contacts_dicts, file, indent=4)

    def load_contacts(self):
        try:
            with open('contacts.json', 'r') as file:
                contacts = json.load(file)
            self.contact_list = [Contact(**contact) for contact in contacts]
        except FileNotFoundError:
            print('Нет сохранённых контактов')

    def delete_contact(self, info):
        contact = self.find_contact(info)
        if contact:
            self.contact_list.remove(contact)
            self.save_contacts()
            print('Контакт удален')
        else:
            print('Контакт не найден')

    def edit_contact(self, edit_dict, info):
        contact = self.find_contact(info)
        if contact:
            for key, value in edit_dict.items():
                if key == 'name':
                    contact.name = value
                elif key == 'phone':
                    contact.phone = value
                elif key == 'email':
                    contact.email = value
            self.save_contacts()
            print('Изменения внесены!')
        else:
            print('Задача не найдена')

    def export_csv(self, filename):
        contacts_dicts = [contact.to_dict() for contact in self.contact_list]
        with open(filename, 'w', newline='') as file:
            dict_writer = csv.DictWriter(file, fieldnames=['contact_id', 'name', 'phone', 'email'])
            dict_writer.writeheader()
            dict_writer.writerows(contacts_dicts)
        print('Данные успешно экспортированы')

    def import_csv(self, filename):
        try:
            with open(filename, 'r', newline='') as file:
                dict_reader = csv.DictReader(file)
                for contact in dict_reader:
                    self.contact_list.append(Contact(**contact))
            self.save_contacts()
            print('Данные успешно импортированы')
        except FileNotFoundError:
            print('Файл не найден...')





class FinanceRecord:
    def __init__(self, fin_id, amount, category, date, description):
        self.fin_id = fin_id
        self.amount = amount
        self.category = category
        self.date = date
        self.description = description

    def to_dict(self):
        return {
            'fin_id': self.fin_id,
            'amount': self.amount,
            'category': self.category,
            'date': self.date,
            'description': self.description,
        }


class FinanceManager:
    def __init__(self):
        self.record_list = []
        self.load_records()

    def find_record(self, record_id):
        for record in self.record_list:
            if record.record_id == record_id:
                return record
        return None

    def add_record(self, amount, category, date, description):
        date = datetime.datetime.strptime(date, '%d-%m-%Y')
        max_id = max((record.record_id for record in self.record_list), default=0) + 1
        new_record = FinanceRecord(max_id, amount, category, date, description)
        self.record_list.append(new_record)
        self.save_records()
        print('Запись добавлена!')

    def list_records(self, category=None, date=None):
        filtered_records = self.record_list
        if category is not None:
            filtered_records = [record for record in filtered_records if record.category == category]
        if date is not None:
            filtered_records = [record for record in filtered_records if record.date <= date]
        for record in filtered_records:
            print(record)

    def generate_report(self, start_date, end_date):
        filtered_records = [record for record in self.record_list if start_date <= record.date <= end_date]
        total_income = sum(record.amount for record in filtered_records if record.amount > 0)
        total_expenses = sum(record.amount for record in filtered_records if record.amount < 0)
        balance = total_income + total_expenses

        print(f'Отчёт за период с {start_date} по {end_date}:')
        print(f'Общий доход: {total_income}')
        print(f'Общий расход: {total_expenses}')
        print(f'Баланс: {balance}')

        category_summary = {}
        for record in filtered_records:
            if record.category not in category_summary:
                category_summary[record.category] = 0
            category_summary[record.category] += record.amount

        print('Сводка по категориям:')
        for category, amount in category_summary.items():
            print(f'{category}: {amount}')

    def save_records(self):
        records_dicts = [record.to_dict() for record in self.record_list]
        with open('finance.json', 'w') as file:
            json.dump(records_dicts, file, indent=4)

    def load_records(self):
        try:
            with open('finance.json', 'r') as file:
                records = json.load(file)
            self.record_list = [FinanceRecord(**record) for record in records]
        except FileNotFoundError:
            print('Нет сохранённых записей')

    def export_csv(self, filename):
        records_dicts = [record.to_dict() for record in self.record_list]
        with open(filename, 'w', newline='') as file:
            dict_writer = csv.DictWriter(file, fieldnames=['record_id', 'amount', 'category', 'date', 'description'])
            dict_writer.writeheader()
            dict_writer.writerows(records_dicts)
        print('Данные успешно экспортированы')

    def import_csv(self, filename):
        try:
            with open(filename, 'r', newline='') as file:
                dict_reader = csv.DictReader(file)
                for row in dict_reader:
                    self.record_list.append(FinanceRecord(**row))
            self.save_records()
            print('Данные успешно импортированы')
        except FileNotFoundError:
            print('Файл не найден...')

    def calculate_balance(self):
        total_income = sum(record.amount for record in self.record_list if record.amount > 0)
        total_expenses = sum(record.amount for record in self.record_list if record.amount < 0)
        balance = total_income + total_expenses
        print(f'Общий баланс: {balance}')





class Calculator:
    def add(self, a, b):
        return a + b

    def subtract(self, a, b):
        return a - b

    def multiply(self, a, b):
        return a * b

    def divide(self, a, b):
        if b == 0:
            return "Деление на ноль недопустимо"
        return a / b

    def calculate(self, expression):
        try:
            expression = expression.replace(" ", "")

            if '+' in expression:
                a, b = expression.split('+')
                return self.add(float(a), float(b))
            elif '-' in expression:
                a, b = expression.split('-')
                return self.subtract(float(a), float(b))
            elif '*' in expression:
                a, b = expression.split('*')
                return self.multiply(float(a), float(b))
            elif '/' in expression:
                a, b = expression.split('/')
                return self.divide(float(a), float(b))
            else:
                return "Неверное выражение"
        except ValueError as e:
            return str(e)
        except Exception as e:
            return f"Ошибка: {e}"




def main_menu():
    print("Добро пожаловать в Персональный помощник!")
    print("Выберите действие:")
    print("1. Управление заметками")
    print("2. Управление задачами")
    print("3. Управление контактами")
    print("4. Управление финансовыми записями")
    print("5. Калькулятор")
    print("6. Выход")

    choice = input("Введите номер действия: ")
    return choice


def manage_notes():
    note_manager = NoteManager()
    while True:
        print("\nУправление заметками:")
        print("1. Создать новую заметку")
        print("2. Просмотреть список заметок")
        print("3. Просмотреть подробности заметки")
        print("4. Редактировать заметку")
        print("5. Удалить заметку")
        print("6. Импортировать из CSV")
        print("7. Экспортировать в CSV")
        print("8. Вернуться в главное меню")
        choice = input("Введите номер действия: ")
        if choice == '1':
            title = input("Введите заголовок новой заметки: ")
            content = input("Введите содержание новой заметки: ")
            note_manager.add_note(title, content)
        elif choice == '2':
            note_manager.list_notes()
        elif choice == '3':
            note_id = int(input('Введите ID заметки, которую хотите просмотреть: '))
            note_manager.view_note(note_id)
        elif choice == '4':
            note_id = int(input('Введите ID заметки, которую хотите редактировать: '))
            new_title = input('Введите новый заголовок: (если не хотите ничего менять, нажмите Enter): ')
            new_content = input('Введите новое содержание (если не хотите ничего менять, нажмите Enter): ')
            edit_dict = {}
            if new_title:
                edit_dict['title'] = new_title
            if new_content:
                edit_dict['content'] = new_content
            note_manager.edit_note(note_id, edit_dict)
        elif choice == '5':
            note_id = int(input('Введите ID заметки, которую хотите удалить: '))
            note_manager.delete_note(note_id)
        elif choice == '6':
            filename = input('Введите имя файла, в который хотите экспортировать: ')
            note_manager.export_csv(filename)
        elif choice == '7':
            filename = input('Введите имя файла, из которого хотите импортировать: ')
            note_manager.import_csv(filename)
        elif choice == '8':
            break
        else:
            print("Неверный выбор. Попробуйте снова...")

def manage_tasks():
    task_manager = TaskManager()
    while True:
        print("\nУправление задачами:")
        print("1. Добавить новую задачу")
        print("2. Просмотреть задачи")
        print("3. Отметить выполненную задачу")
        print("4. Редактировать задачу")
        print("5. Удалить задачу")
        print("6. Импортировать из CSV")
        print("7. Экспортировать в CSV")
        print("8. Вернуться в главное меню")
        choice = input("Введите номер действия: ")
        if choice == '1':
            title = input("Введите название новой задачи: ")
            description = input("Введите описание новой задачи: ")
            prior = input("Введите приоритет задачи: \n1. Высокий \n2. Средний \n3. Низкий: ")
            if prior == '1': priority = 'Высокий'
            elif prior == '2': priority = 'Средний'
            elif prior == '3': priority = 'Низкий'
            else: print('Неверный выбор...')
            due_date = input("Введите дату окончания задачи (ДД-ММ_ГГГГ): ")
            task_manager.add_task(title, description, priority, due_date)
        elif choice == '2':
            st = input('Отфильтровать задачи по статусу? (0 - нет, 1 - да): ')
            pr = input('Отфильтровать задачи по приоритету? (0 - нет, 1 - да): ')
            dt = input('Отфильтровать задачи по дате? (0 - нет, 1 - да): ')
            status = 1 if st == '1' else None
            priority = 1 if pr == '1' else None
            due_date = 1 if dt == '1' else None
            task_manager.show_list_tasks(status, priority, due_date)
        elif choice == '3':
            task_id = int(input('Введите ID заметки, которую хотите отметить как выполненную: '))
            task_manager.change_done(task_id)
        elif choice == '4':
            task_id = int(input('Введите ID задачи, которую хотите редактировать: '))
            new_title = input('Введите новое название: (если не хотите ничего менять, нажмите Enter): ')
            new_description = input('Введите новое описание (если не хотите ничего менять, нажмите Enter): ')
            pr = input('Введите новое статус: \n1. Высокий \n2. Средний \n3. Низкий \nEnter - не менять статус: ')
            new_date = input('Введите новую дату (если не хотите ничего менять, нажмите Enter): ')
            edit_dict = {}
            if pr == '1': new_priority = 'Высокий'
            elif pr == '2': new_priority = 'Средний'
            elif pr == '3': new_priority = 'Низкий'
            else: new_priority=None
            if new_title:
                edit_dict['title'] = new_title
            if new_description:
                edit_dict['description'] = new_description
            if new_priority:
                edit_dict['priority'] = new_priority
            if new_date:
                edit_dict['due_date'] = new_date
            task_manager.edit_task(task_id, edit_dict)
        elif choice == '5':
            task_id = int(input('Введите ID задачи, которую хотите удалить: '))
            task_manager.delete_task(task_id)
        elif choice == '6':
            filename = input('Введите имя файла, в который хотите экспортировать: ')
            task_manager.export_csv(filename)
        elif choice == '7':
            filename = input('Введите имя файла, з которого хотите импортировать: ')
            task_manager.import_csv(filename)
        elif choice == '8':
            break
        else:
            print("Неверный выбор. Попробуйте снова...")

def manage_contacts():
    contact_manager = ContactManager()
    while True:
        print("\nУправление контактами:")
        print("1. Добавить новый контакт")
        print("2. Найти контакт")
        print("3. Редактировать контакт")
        print("4. Удалить контакт")
        print("5. Импортировать из CSV")
        print("6. Экспортировать в CSV")
        print("7. Вернуться в главное меню")
        choice = input("Введите номер действия: ")
        if choice == '1':
            name = input("Введите имя контакта: ")
            phone = input("Введите телефон контакта: ")
            email = input("Введите email контакта: ")
            contact_manager.add_contact(name, phone, email)
        elif choice == '2':
            info = input('Введите имя или номер телефона контакта: ')
            contact_manager.find_contact(info)
        elif choice == '3':
            info = input('Введите имя или номер телефона контакта: ')
            new_name = input('Введите новое имя контакта: (если не хотите ничего менять, нажмите Enter): ')
            new_phone = input('Введите новый номер контакта: (если не хотите ничего менять, нажмите Enter): ')
            new_email = input('Введите новую почту контакта: (если не хотите ничего менять, нажмите Enter): ')
            edit_dict = {}
            if new_name:
                edit_dict['name'] = new_name
            if new_phone:
                edit_dict['phone'] = new_phone
            if new_email:
                edit_dict['email'] = new_email
            contact_manager.edit_contact(edit_dict, info)
        elif choice == '4':
            info = input('Введите имя или номер контакта, которого хотите удалить: ')
            contact_manager.delete_contact(info)
        elif choice == '5':
            filename = input('Введите имя файла, в который хотите экспортировать: ')
            contact_manager.export_csv(filename)
        elif choice == '6':
            filename = input('Введите имя файла, з которого хотите импортировать: ')
            contact_manager.import_csv(filename)
        elif choice == '7':
            break
        else:
            print("Неверный выбор. Попробуйте снова...")

def manage_finance():
    finance_manager = FinanceManager()
    while True:
        print("\nУправление финансовыми записями:")
        print("1. Добавить новую запись")
        print("2. Просмотреть записи")
        print("3. Сгенерировать отчёт")
        print("4. Импортировать из CSV")
        print("5. Экспортировать в CSV")
        print("6. Вернуться в главное меню")
        choice = input("Введите номер действия: ")
        if choice == '1':
            amount = float(input("Введите сумму (положительное число для доходов, отрицательное для расходов): "))
            category = input("Введите категорию: ")
            date = input("Введите дату (ДД-ММ-ГГГГ): ")
            description = input("Введите описание: ")
            finance_manager.add_record(amount, category, date, description)
        elif choice == '2':
            dt = input('Введите дату, до которой хотите посмотреть список операций (ДД-ММ-ГГГГ) (или Enter - если все операции): ')
            date = datetime.datetime.strptime(dt, '%d-%m-%Y')
            ctg = input('Введите категорию, в которой хотите посмотреть список операций (или Enter - если все операции): ')
            finance_manager.list_records(ctg, date)
        elif choice == '3':
            st_date = input('Введите начальную дату (ДД-ММ-ГГГГ): ')
            end_date = input('Введите конечную дату (ДД-ММ-ГГГГ): ')
            finance_manager.generate_report(st_date, end_date)
        elif choice == '4':
            filename = input('Введите имя файла, в который хотите экспортировать: ')
            finance_manager.export_csv(filename)
        elif choice == '5':
            filename = input('Введите имя файла, з которого хотите импортировать: ')
            finance_manager.import_csv(filename)
        elif choice == '6':
            break
        else:
            print("Неверный выбор. Попробуйте снова...")

def calculator():
    calculator = Calculator()
    while True:
        print("\nКалькулятор:")
        print("1. Выполнить вычисление")
        print("2. Вернуться в главное меню")
        choice = input("Введите номер действия: ")
        if choice == '1':
            expression = input("Введите выражение (например, 2*2): ")
            result = calculator.calculate(expression)
            print(f"Результат: {result}")
        elif choice == '2':
            break
        else:
            print("Неверный выбор. Попробуйте снова...")

def main():
    while True:
        choice = main_menu()
        if choice == '1':
            manage_notes()
        elif choice == '2':
            manage_tasks()
        elif choice == '3':
            manage_contacts()
        elif choice == '4':
            manage_finance()
        elif choice == '5':
            calculator()
        elif choice == '6':
            print("Выход... Всего хорошего!)")
            break
        else:
            print("Неверный выбор. Попробуйте снова...")


if __name__ == "__main__":
    main()