from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from dotenv import load_dotenv
import os

load_dotenv()

conf = ConnectionConfig(
    MAIL_USERNAME=os.getenv("MAIL_USERNAME"),
    MAIL_PASSWORD=os.getenv("MAIL_PASSWORD"),
    MAIL_FROM=os.getenv("MAIL_FROM"),
    MAIL_PORT=int(os.getenv("MAIL_PORT", 587)),
    MAIL_SERVER=os.getenv("MAIL_SERVER"),
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
    USE_CREDENTIALS=True
)

async def send_welcome_email(email: str, name: str):
    message = MessageSchema(
        subject="Welcome to Employee Management System!",
        recipients=[email],
        body=f"""
        <h2>Welcome {name}!</h2>
        <p>Your account has been created successfully.</p>
        <p>You can now login to the Employee Management System.</p>
        <br>
        <p>Best regards,</p>
        <p>HR Team</p>
        """,
        subtype="html"
    )
    fm = FastMail(conf)
    await fm.send_message(message)

async def send_employee_added_email(admin_email: str, employee_name: str):
    message = MessageSchema(
        subject="New Employee Added",
        recipients=[admin_email],
        body=f"""
        <h2>New Employee Added!</h2>
        <p>A new employee <b>{employee_name}</b> has been 
        added to the system.</p>
        <br>
        <p>Best regards,</p>
        <p>Employee Management System</p>
        """,
        subtype="html"
    )
    fm = FastMail(conf)
    await fm.send_message(message)

async def send_document_summary_email(
    email: str, 
    filename: str, 
    summary: str
):
    message = MessageSchema(
        subject=f"Document Summary: {filename}",
        recipients=[email],
        body=f"""
        <h2>Document Summary</h2>
        <p><b>File:</b> {filename}</p>
        <br>
        <h3>AI Summary:</h3>
        <p>{summary}</p>
        <br>
        <p>Best regards,</p>
        <p>Employee Management System</p>
        """,
        subtype="html"
    )
    fm = FastMail(conf)
    await fm.send_message(message)