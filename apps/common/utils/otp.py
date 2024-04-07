import pyotp
from datetime import datetime, timedelta
from django.template.loader import render_to_string

# Apps
from apps.common.utils import send_email
from .protect_data import ProtectData


class OTP:
    def __init__(self, profile):
        self.code = None
        self.user = profile.user
        self.profile = profile
        self.time_format = "%Y-%m-%d %H:%M:%S"
        self.date_email = datetime.now().strftime(self.time_format)
        self.exp_date = datetime.now() + timedelta(seconds=180)

        decrypt_o_key = ProtectData(encrypted_data=self.profile.o_key).decrypt()
        self.totp = pyotp.TOTP(s=decrypt_o_key, interval=180)

    def create_and_send_otp(self):
        """Create OTP code with expiration of 3 min."""

        try:
            self.code = self.totp.now()
            self.send_email_otp_code()

        except Exception as e:
            print('Error OPT:', e)
            raise Exception("Can't create OTP code.")

    def send_email_otp_code(self):
        """Send email with OTP."""

        try:
            email_context = {
                'body': f"Hi {self.user.username}! Write the code in the NiiMX registry to verify the account.",
                'date': self.date_email,
                'exp_date': self.exp_date.strftime(self.time_format),
                'otp': self.code
            }

            msg_html = render_to_string(
                'emails/account-verify.html',
                email_context
            )

            email_data = {
                'from': 'ACLIVE <noreply@aclive.io>',
                'to': [self.user.email],
                'subject': 'ACLIVE - Account Verification',
                'html': msg_html,
            }
            send_email(email_data)

        except Exception as e:
            print('Error send OTP:', e)
            raise Exception("Can't send OTP email.")

    def verify(self, code: str,):
        """OTP code verification."""
        return self.totp.verify(code)

