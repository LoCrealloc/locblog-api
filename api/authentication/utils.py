from ssl import create_default_context
from smtplib import SMTP, SMTPException
from email.message import EmailMessage
from email.headerregistry import Address
from secrets import randbelow
import re

from api.config import smtp_user, smtp_password, smtp_server, smtp_port


def check_password(password: str) -> bool:
    return True


def check_email(email: str) -> bool:
    return True if re.match(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", email) else False


def send_validation_email(email: str, username: str) -> str:
    mail = EmailMessage()

    mail["From"] = Address(display_name="LoCblog", addr_spec=smtp_user)
    mail["To"] = Address(addr_spec=email)
    mail["Subject"] = "Validation email"

    secret_digits = "".join([str(randbelow(10)) for _ in range(6)])

    with open("authentication/mail_templates/register.html", "r") as template_file:
        template = template_file.read()

    with open("authentication/mail_templates/register.txt", "r") as template_text_file:
        template_text = template_text_file.read()

    mail.set_content(template_text.format(user=username, code=secret_digits))
    mail.add_alternative(template.format(user=username, code=secret_digits), subtype="html")

    context = create_default_context()

    server: SMTP | None = None

    try:
        server = SMTP(smtp_server, int(smtp_port))
        server.starttls(context=context)
        server.login(user=smtp_user, password=smtp_password)

        server.send_message(mail)

    except SMTPException as e:
        # TODO: handle smtp errors
        raise e

    finally:
        if server:
            server.quit()

    return secret_digits
