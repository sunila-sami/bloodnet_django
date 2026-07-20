# BloodNet update

Implemented:

- Django token-based forgot-password flow from the login page.
- Password reset email in plain-text and styled HTML formats.
- Password reset link expiry setting (`PASSWORD_RESET_TIMEOUT`, default 1 hour).
- Show/hide password eye icon on login and new-password forms.
- Landing-page **Request Blood** button now opens account creation.
- Animated hover/focus effect for navbar links.
- Navbar **About** link now scrolls to the existing Emergency Help + statistics row (no new About section added).
- Navbar **How it Works** link now scrolls to the existing workflow section with smooth scrolling.
- Show/hide password eye icons added to both signup password fields.
- Authentication tests for login UI, landing redirect, and complete password reset flow.

Validation completed:

```text
python manage.py check
System check identified no issues.

python manage.py test accounts
Ran 3 tests — OK.
```
