from django.core.mail import send_mail
from datetime import datetime, timedelta
from django.template.loader import render_to_string


def send_email(data):
    return send_mail(
        data['subject'],
        None,
        data['from'],
        data['to'],
        fail_silently=False,
        html_message=data['html'],
    )


class Email:
    @staticmethod
    def send(payload):
        """Built email to send."""
        try:
            email_context = {
                **payload['context'],
                'created_date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            }
            msg_html = render_to_string(
                payload['html'],
                email_context
            )
            email_data = {
                'from': 'MentorAIBot <noreply@driftibot.com>',
                'to': payload['to'],
                'subject': payload['subject'],
                'html': msg_html,
            }
            send_email(email_data)

        except Exception as e:
            print('Error send Email:', e)
            raise Exception("Can't send email.")
