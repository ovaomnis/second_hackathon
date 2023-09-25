from config.celery import app

from.services import send_activation_code, send_code_forgot_password

@app.task
def celery_send_activation_code(email, code):
    send_activation_code(email, code)


@app.task
def celery_send_code_forgot_password(email, code):
    send_code_forgot_password(email, code)
