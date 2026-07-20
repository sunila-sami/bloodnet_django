# BloodNet — Django

BloodNet includes a real signup → Gmail OTP verification → login flow.

## Verification flow

1. User submits the signup form and is saved with `is_verified=False`.
2. A 6-digit OTP is generated.
3. Django emails the OTP to the signup email address.
4. User enters the OTP on the verification page.
5. A correct OTP sets `is_verified=True` and redirects to login.
6. An unverified user who tries to log in receives a fresh OTP.

## 1. Install and prepare the project

```bash
python -m venv venv
```

Activate the environment on Windows:

```powershell
venv\Scripts\activate
```

Install the dependencies:

```bash
pip install -r requirements.txt
```

## 2. Configure Gmail SMTP

Gmail requires a Google **App Password**, not your normal Gmail password.
Enable 2-Step Verification for the sender Google account, then create an App
Password for BloodNet.

Edit `.env` and replace the example values:

```env
DJANGO_SECRET_KEY=replace-with-a-long-random-secret-key
DJANGO_DEBUG=True
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1

EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_USE_SSL=False
EMAIL_HOST_USER=yourgmail@gmail.com
EMAIL_HOST_PASSWORD=your-16-character-google-app-password
DEFAULT_FROM_EMAIL=BloodNet <yourgmail@gmail.com>
```

Important:

- Use the 16-character Google App Password, not the Gmail account password.
- Do not upload `.env` to GitHub. It is already included in `.gitignore`.
- Spaces copied with the App Password are removed automatically by settings.
- If Gmail credentials are absent, the project falls back to console email so
  development can continue.

## 3. Create database tables

```bash
python manage.py migrate
```
## 5. Run BloodNet

```bash
python manage.py runserver
```

Open:

- `http://127.0.0.1:8000/`
- `http://127.0.0.1:8000/accounts/signup/`
- `http://127.0.0.1:8000/accounts/login/`
- `http://127.0.0.1:8000/admin/`

## Email configuration files

- `bloodnet_project/settings.py` — loads SMTP configuration from `.env`.
- `.env.example` — safe template for your credentials.
- `.env` — your private Gmail address and App Password; create locally.
- `accounts/views.py` — sends styled OTP email and handles delivery errors.
- `accounts/management/commands/test_email.py` — SMTP test command.

## Troubleshooting

### OTP still appears in terminal

Django could not find both `EMAIL_HOST_USER` and `EMAIL_HOST_PASSWORD`. Confirm
that the file is named exactly `.env`, is beside `manage.py`, and restart
`runserver` after saving it.

### Username and Password not accepted

Use a Google App Password. Do not use your normal Gmail password. Confirm that
2-Step Verification is enabled for the sender account.

### Connection timed out

A firewall, VPN, hosting provider or network may be blocking SMTP port 587.
Try another network or use a transactional email service for deployment.

### Account created but email failed

BloodNet now shows a clear error instead of crashing. Correct the `.env`
settings, restart the server and select **Resend Code** on the verification page.

## Forgot password flow

1. Select **Forgot Password?** on the login page.
2. Enter the email address registered with BloodNet.
3. Django emails a secure, one-time reset link.
4. Open the link and enter the new password twice.
5. After success, return to login with the new password.

The reset link expires after 1 hour by default. You can change this in `.env`:

```env
PASSWORD_RESET_TIMEOUT=3600
```

For local development without Gmail credentials, the reset email and link are printed in the terminal by Django's console email backend.
