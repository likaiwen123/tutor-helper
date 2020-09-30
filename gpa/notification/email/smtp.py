import smtplib
from notification.email.content import User
from email.message import EmailMessage
from email.headerregistry import Address


class SMTPSender:
    def __init__(self, server, port, user, password, sender=None):
        if sender is None:
            sender = (user.split("@")[0], user)
        self.sender = sender
        self.account = (user, password)
        self.server = (server, port)
        self.smtp = None

    def connect(self, starttls=False):
        self.smtp = smtplib.SMTP_SSL(self.server[0], self.server[1])
        self.smtp.login(self.account[0], self.account[1])
        if starttls:
            self.smtp.starttls()

    def send(self, messages, subject, quit_after_sent=True):
        for message in messages:
            msg = EmailMessage()
            msg['Subject'] = subject
            msg['From'] = Address(self.sender[0], self.account[0].split("@")[0], self.account[0].split("@")[1])
            # msg['To'] = Address(display_name='李凯文', username='likw18', domain='mails.tsinghua.edu.cn')
            # msg['To'] = msg['From']
            msg['To'] = Address(message.receiver.name,
                                message.receiver.email.split("@")[0],
                                message.receiver.email.split("@")[1])

            msg.set_content(message.content)
            msg.add_alternative(message.content, subtype='html')
            try:
                self.smtp.send_message(msg)
            except Exception:
                print(Exception)
                exit(1)

        if quit_after_sent:
            self.smtp.quit()
