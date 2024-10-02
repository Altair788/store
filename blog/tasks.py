from django.core.mail import send_mail

from config.settings import EMAIL_HOST_USER


def send_notification_email(article_title, views_counter):
    subject = f"Поздравляем! Ваша статья '{article_title}' достигла 100 просмотров!"
    message = f"Статья '{article_title}' теперь имеет {views_counter} просмотров."
    from_email = EMAIL_HOST_USER
    recipient_list = [from_email]

    send_mail(subject, message, from_email, recipient_list)