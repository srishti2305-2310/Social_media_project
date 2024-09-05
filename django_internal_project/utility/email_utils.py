import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from django.template.loader import render_to_string

from intern_network.settings import EmailConstants


def send_email(subject, plain_text_body, template_name, context, to_email):
    sender_email = EmailConstants.EMAIL_HOST_USER
    password = EmailConstants.EMAIL_HOST_PASSWORD

    # Render the HTML template with context
    html_body = render_to_string(template_name, context)

    # Set up the MIME
    message = MIMEMultipart('alternative')
    message['From'] = sender_email
    message['To'] = to_email
    message['Subject'] = subject

    # Attach the plain text and HTML versions of the email body
    part1 = MIMEText(plain_text_body, 'plain')
    part2 = MIMEText(html_body, 'html')

    message.attach(part1)
    message.attach(part2)

    try:
        # Set up the server
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()  # Enable security

        # Login to the server
        server.login(sender_email, password)

        # Send the email
        server.sendmail(sender_email, to_email, message.as_string())
        print("Email sent successfully")

    except Exception as e:
        print(f"Error: {e}")

    finally:
        # Terminate the session
        server.quit()
