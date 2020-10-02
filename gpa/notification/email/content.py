import pandas as pd
import notification.email.template as tpt
import HtmlTable.HTML as HTML


class User:
    def __init__(self, name, email):
        self.name = name
        self.email = email

    def __str__(self):
        return "{}<{}>".format(self.name, self.email)


class Message:
    def __init__(self, name, email_address, data):
        self.receiver = User(name, email_address)
        self._data = data
        self.content = ""

    def prepare(self, template, class_number, grade_number, sender):
        table = TableBuilder(self._data).build()
        self.content = template.replace("<name>", self.receiver.name).replace("<class number>", str(class_number)).\
            replace("<grade number>", str(grade_number)).replace("<GPA table>", str(table)).\
            replace("<sender name>", sender)


class TableBuilder:
    def __init__(self, data):
        self.data = data

    def build(self):
        table = HTML.Table()
        for key in self.data.index:
            value = self.data[key]
            if isinstance(value, float) and value <= 4:
                value = "{:.4}".format(value)
            data = [key, value]

            table_row = HTML.TableRow(cells=data, col_align=['center'] * len(data),
                                      col_valign=['center'] * len(data))
            table.rows.append(table_row)
        return table


class ClassMessages:
    def __init__(self, class_name, contact_file, data, grade_number, template=None):
        contacts = pd.DataFrame(pd.read_csv(contact_file))
        self.contacts = {}
        name_entry = "姓名"
        email_entry = "电子邮件地址"
        for i in range(len(contacts)):
            name = contacts.iloc[i][name_entry]
            if name in self.contacts:
                # raise ValueError("Duplicate names detected: {}".format(name))
                print("Warning: Duplicate names detected: {}".format(name))
            self.contacts[name] = contacts.iloc[i][email_entry]

        self.number = len(data)
        self.data = data
        self.grade_number = grade_number
        if template is None:
            self.template = tpt.basic_template
        else:
            self.template = template

    def build(self, sender):
        messages = []
        for i in range(self.number):
            slice = self.data.iloc[i]
            name = slice["姓名"]
            if name in self.contacts:
                email = self.contacts[name]
            else:
                raise ValueError("Failed to get the email address of user {}".format(name))
            msg = Message(name, email, slice)
            msg.prepare(template=self.template, class_number=self.number, grade_number=self.grade_number,
                        sender=sender)
            messages.append(msg)
        return messages
