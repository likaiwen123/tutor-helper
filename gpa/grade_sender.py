import pandas as pd
from gpa.notification.email.content import ClassMessages
from gpa.notification.email.smtp import SMTPSender

rank_file = "ranks.xlsx"
class_name = "工物80"
contact_file = "address.csv"
grade_number = 134

# SMTP settings
server = "mails.tsinghua.edu.cn"
port = 465
user = "your Tsinghua Email address"  # for example, abc18@mails.tsinghua.edu.cn
password = "your password"  # DO NOT push your real password to your fork or any public places.

# The name displayed in the email
display_name = "李凯文"
sender_name = "李凯文"

# The customized template of the email content.
template = None

if __name__ == "__main__":
    data = pd.read_excel(rank_file, sheet_name=class_name, index_col=0)
    messages = ClassMessages(class_name, contact_file, data, grade_number=grade_number,
                             template=template).build(sender=sender_name)
    sender = SMTPSender(server, port, user, password, sender=display_name)
    sender.connect()
    sender.send(subject="大三上成绩通知", messages=messages, dry_run=False)
