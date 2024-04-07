from apps.common.utils import OTP


def send_otp_email(profile):
    """Send email with OTP code to account verification."""
    try:
        otp = OTP(profile)
        otp.create_and_send_otp()
        return True
    except Exception as e:
        print(f'Cannot sent OTP email: {e}')
        return False
