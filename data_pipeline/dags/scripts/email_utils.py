from airflow.models import Variable
import smtplib
from email.mime.text import MIMEText
from jinja2 import Template  
from email.mime.multipart import MIMEMultipart

def send_success_email(param1, param2, **kwargs):
    """
    Sends a success notification email to a predefined list of recipients when an Airflow DAG completes successfully.

    Args:
        **kwargs: Arbitrary keyword arguments containing Airflow context, including:
            - dag: The DAG object associated with the successful execution.
            - task: The task object associated with the successful execution.

    Environment Variables:
        EMAIL_USER: The sender's email address.
        EMAIL_PASSWORD: The password for the sender's email account.

    Sends an email to the recipients with the DAG and task details upon successful execution.
    """
    sender_email = Variable.get('EMAIL_USER')
    password = Variable.get('EMAIL_PASSWORD')
    receiver_emails = ["vadhaiya.r@northeastern.edu", "bilwal.s@northeastern.edu", "kushalshankar03@gmail.com", "shah.rajiv1702@gmail.com"]

    # Define subject and body templates
    subject_template = 'Airflow Success: {{ dag.dag_id }} - Data Pipeline tasks succeeded'
    body_template = '''Hi team,
    The Data Pipeline tasks in DAG {{ dag.dag_id }} succeeded.'''
    
    # Render templates using Jinja2 Template
    subject = Template(subject_template).render(dag=kwargs['dag'], task=kwargs['task'])
    body = Template(body_template).render(dag=kwargs['dag'], task=kwargs['task'])

    # Ensure UTF-8 encoding
    subject = subject.encode('utf-8').decode('utf-8')
    body = body.encode('utf-8').decode('utf-8')

    # Create the email headers and content
    email_message = MIMEMultipart()
    email_message['Subject'] = subject
    email_message['From'] = sender_email
    email_message['To'] = ", ".join(receiver_emails).encode('utf-8').strip()

    # Add body to email
    email_message.attach(MIMEText(body, 'plain', 'UTF-8'))

    try:
        # Set up the SMTP server
        server = smtplib.SMTP('smtp.gmail.com', 587)  # Using Gmail's SMTP server
        server.starttls()  # Secure the connection
        server.login(sender_email, password)
        
        print('Server logged IN')
        # Send email to each receiver
        for receiver_email in receiver_emails:
            email_message.replace_header('To', receiver_email)
            server.sendmail(sender_email, receiver_email, email_message.as_string())
            print(f"Success email sent successfully to {receiver_email}!")

    except Exception as e:
        print(f"Error sending success email: {e}")
    finally:
        server.quit()


def send_failure_email(task_instance, exception):
    """
    Sends a failure notification email to a predefined recipient when an Airflow task fails.

    Args:
        task_instance (TaskInstance): The Airflow TaskInstance object representing the failed task.
        exception (Exception): The exception raised during task execution.

    Environment Variables:
        EMAIL_USER: The sender's email address.
        EMAIL_PASSWORD: The password for the sender's email account.

    Sends an email containing the DAG ID, task ID, and exception details to the specified recipient.
    """
    sender_email = Variable.get('EMAIL_USER')
    receiver_email = "vadhaiya.r@northeastern.edu"
    password = Variable.get('EMAIL_PASSWORD')

    # Subject and body for the failure email
    subject_template = 'Airflow Failure: {{ task_instance.dag_id }} - {{ task_instance.task_id }}'
    body_template = 'The task {{ task_instance.task_id }} in DAG {{ task_instance.dag_id }} has failed. Exception: {{ exception }}'

    # Render templates using Jinja2 Template
    subject = Template(subject_template).render(task_instance=task_instance)
    body = Template(body_template).render(task_instance=task_instance, exception=str(exception))

    # Create the email headers and content
    email_message = MIMEText(body, 'html')
    email_message['Subject'] = subject
    email_message['From'] = sender_email
    email_message['To'] = receiver_email

    try:
        # Set up the SMTP server
        server = smtplib.SMTP('smtp.gmail.com', 587)  # Using Gmail's SMTP server
        server.starttls()  # Secure the connection
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, email_message.as_string())
        print("Failure email sent successfully!")
    except Exception as e:
        print(f"Error sending failure email: {e}")
    finally:
        server.quit()