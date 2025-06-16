from app.models.BaseModel import BaseModel
from email_validator import validate_email, EmailNotValidError

class User(BaseModel):

    def __init__(self, first_name, last_name, email, is_admin):
        super().__init__()

        # ✅ Validate parameters,with attributes
        if len(first_name) > 50:
            raise ValueError("First name: Required, maximum length of 50 characters.")
        if len(last_name) > 50:
            raise ValueError("Last name: Required, maximum length of 50 characters.")
        if not self._is_valid_email(email):
            raise ValueError("Invalid email format.")
        if email in User.used_emails:
            raise ValueError("Email already in use.")
        if not self.is_admin_user():
            raise PermissionError("Access denied. Admin privileges required.")



        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.is_admin = bool(is_admin)

        # ✅ save email
        User.used_emails.add(email)

    def _is_valid_email(self, email):
        try:
            validate_email(email)
            return True
        except EmailNotValidError:
            return False


    def is_admin_user(self):
        return self.is_admin
