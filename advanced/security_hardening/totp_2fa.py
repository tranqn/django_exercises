"""
TOTP-based 2FA (compatible with Google Authenticator / Authy).

pip install pyotp qrcode
"""

import pyotp


def new_secret():
    return pyotp.random_base32()


def provisioning_uri(secret, username, issuer="MySite"):
    return pyotp.totp.TOTP(secret).provisioning_uri(
        name=username, issuer_name=issuer
    )


def verify_code(secret, code):
    # valid_window=1 tolerates ~30s clock drift either side.
    return pyotp.TOTP(secret).verify(code, valid_window=1)