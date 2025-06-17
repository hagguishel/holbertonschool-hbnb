#!/usr/bin/python3

from app.models.BaseModel import BaseModel
from email_validator import validate_email, EmailNotValidError

class User(BaseModel):

    def __init__(self, first_name, last_name, email, password, is_admin):
        super().__init__()
    
        User.used_emails.add(self._email)

        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.is_admin = bool(is_admin)
        self.password = password

        if not self.is_admin_user:
            raise PermissionError("Access denied. Admin privileges required.")

        User.used_emails.add(self._email)

    @property
    def first_name(self):
        return self._first_name

    @first_name.setter
    def first_name(self, value):
        if not value or len(value) > 50:
            raise ValueError("First name: Required, maximum length of 50 characters.")
        self._first_name = value

    @property
    def last_name(self):
        return self._last_name

    @last_name.setter
    def last_name(self, value):
        if not value or len(value) > 50:
            raise ValueError("Last name: Required, maximum length of 50 characters.")
        self._last_name = value

     @property
    def email(self):
        return self._email

    @email.setter
    def email(self, value):
        if not self._is_valid_email(value):
            raise ValueError("Invalid email format.")
        if value in User.used_emails:
            raise ValueError("Email already in use.")
        self._email = value

    def _is_valid_email(self, email):
        try:
            validate_email(email)
            return True
        except EmailNotValidError:
            return False
        
    @property
    def is_admin(self):
        return self._is_admin

    @is_admin.setter
    def is_admin(self, value):
        self._is_admin = bool(value)



    def is_admin_user(self):
        return self.is_admin
    
    @property
    def password(self):
        return self.password
    
    @password.setter
    def password(self, value):

    


    def to_dict(self):
        return{
        "id": self.id,
        "first_name": self.first_name,
        "last_name": self.last_name,
        "email": self.email,
        "password": self.password,
        "is_admin": self.is_admin_user}