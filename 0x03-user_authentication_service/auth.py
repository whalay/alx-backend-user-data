#!/usr/bin/env python3
""" This module contains methods for authentication """
import bcrypt
import uuid
from db import DB
from user import User


def _hash_password(password: str) -> bytes:
    # Generate a random salt and hash the password
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode('utf-8'), salt)

def _generate_uuid() -> str:
    """ generates a uuid """
    return str(uuid.uuid4())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        """ initializes self """
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """ registers a user """
        try:
            user = self._db.find_user_by(email=email)
        except Exception:
            return self._db.add_user(email, _hash_password(password))

        raise ValueError(f'User {email} already exists')

    def valid_login(self, email: str, password: str) -> bool:
        """ validates user credentials """
        try:
            user = self._db.find_user_by(email=email)
        except Exception:
            return False

        return bcrypt.checkpw(password.encode('utf-8'), user.hashed_password)

    def create_session(self, email: str) -> str:
        """ creates a session id for a user """
        try:
            user = self._db.find_user_by(email=email)
        except Exception:
            return None
        if user:
            session_id = _generate_uuid()
            self._db.update_user(user.id, session_id=session_id)
            return session_id

    def get_user_from_session_id(self, session_id: str) -> User:
        """ returns the corresponding user with a session id or none """
        if session_id:
            try:
                return self._db.find_user_by(session_id=session_id)
            except Exception:
                return None

    def destroy_session(self, user_id: int) -> None:
        """ destroys a user session """
        self._db.update_user(user_id, session_id=None)

    def get_reset_password_token(self, email: str) -> str:
        """ generates a reset password token """
        try:
            user = self._db.find_user_by(email=email)
        except Exception:
            raise ValueError

        reset_token = _generate_uuid()
        self._db.update_user(user.id, reset_token=reset_token)
        return reset_token

    def update_password(self, reset_token: str, password: str) -> None:
        """ updates a users password """
        try:
            user = self._db.find_user_by(reset_token=reset_token)
        except Exception:
            raise ValueError

        self._db.update_user(user.id,
                             hashed_password=_hash_password(password),
                             reset_token=None)
