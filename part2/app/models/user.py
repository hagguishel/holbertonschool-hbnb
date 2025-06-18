#!/usr/bin/python3

from app.models.basemodel import BaseModel
from email_validator import validate_email, EmailNotValidError

class User(BaseModel):
    used_emails = set()

    def __init__(self, first_name, last_name, email, is_admin=False):
        super().__init__()

        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.is_admin = bool(is_admin)

        User.used_emails.add(self.email)

    @property
    def first_name(self):
        return self.__first_name

    @first_name.setter
    def first_name(self, value):
        if not value or len(value) > 50:
            raise ValueError("First name: Required, maximum length of 50 characters.")
        self.__first_name = value

    @property
    def last_name(self):
        return self.__last_name

    @last_name.setter
    def last_name(self, value):
        if not value or len(value) > 50:
            raise ValueError("Last name: Required, maximum length of 50 characters.")
        self.__last_name = value

    @property
    def email(self):
        return self.__email

    @email.setter
    def email(self, value):
        if not self._is_valid_email(value):
            raise ValueError("Invalid email format.")
        if value in User.used_emails:
            raise ValueError("Email already in use.")
        self.__email = value

    def _is_valid_email(self, email):
        try:
            validate_email(email, check_deliverability=False)
            return True
        except EmailNotValidError as e:
            print(f"Email validation error: {e}")
            return False

        
    @property
    def is_admin(self):
        return self.__is_admin

    @is_admin.setter
    def is_admin(self, value):
        self.__is_admin = bool(value)


    @property
    def is_admin_user(self):
        return self.__is_admin
    
   
    def to_dict(self):
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email
        }
