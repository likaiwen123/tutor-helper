import pandas as pd
from notification.email.content import ClassMessages
from notification.email.smtp import SMTPSender

rank_file = "ranks.xlsx"
class_name = "工物80"
contact_file = "address.csv"
grade_number = 134

server = "mails.tsinghua.edu.cn"
port = 465
user = "your Tsinghua Email address"  # for example, abc18@mails.tsinghua.edu.cn
password = "your password"  # DO NOT push your real password to your fork or any public places.

name = "Kaiwen Li"

if __name__ == "__main__":
    data = pd.read_excel(rank_file, sheet_name=class_name, index_col=0)
    messages = ClassMessages(class_name, contact_file, data, grade_number=grade_number).build()
    sender = SMTPSender(server, port, user, password)
    sender.connect()
    sender.send(subject="大二成绩通知", messages=messages)
