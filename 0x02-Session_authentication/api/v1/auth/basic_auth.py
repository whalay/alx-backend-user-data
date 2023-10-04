#!/usr/bin/env python3
""" A basic authentication class """
import base64
from api.v1.auth.auth import Auth
from models.user import User
from typing import TypeVar


class BasicAuth(Auth):
    """ a basic auth class """

    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """ extracts the base64 authorization header """
        if authorization_header is None:
            return None
        if type(authorization_header) is not str:
            return None
        if not authorization_header.startswith('Basic '):
            return None

        return authorization_header[6:]

    def decode_base64_authorization_header(
        self,
        base64_authorization_header: str
    ) -> str:
        """ decodes the base64 authorization header """
        if base64_authorization_header is None:
            return None
        if type(base64_authorization_header) is not str:
            return None
        try:
            byte_st = base64.b64decode(base64_authorization_header)
            return byte_st.decode('utf-8')
        except Exception:
            return None

    def extract_user_credentials(
        self,
        decoded_base64_authorization_header: str
    ) -> (str, str):
        """ extracts the user credentials """
        if decoded_base64_authorization_header is None:
            return None, None
        if type(decoded_base64_authorization_header) is not str:
            return None, None
        if ':' not in decoded_base64_authorization_header:
            return None, None
        return tuple(decoded_base64_authorization_header.split(':', 1))

    def user_object_from_credentials(self,
                                     user_email: str,
                                     user_pwd: str) -> TypeVar('User'):
        """ returns the User instance based on his email and password """
        if user_email is None or type(user_email) is not str:
            return None
        if user_pwd is None or type(user_pwd) is not str:
            return None
        try:
            users = User.search({'email': user_email})
        except Exception:
            return None
        for user in users:
            if user.is_valid_password(user_pwd):
                return user
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """ retrieves the User instance for a request """
        auth_header = self.authorization_header(request)
        if auth_header is None:
            return None
        b64_auth_header = self.extract_base64_authorization_header(auth_header)
        if b64_auth_header is None:
            return None
        decoded_auth_header = self.decode_base64_authorization_header(
            b64_auth_header
        )
        if decoded_auth_header is None:
            return None
        user_credentials = self.extract_user_credentials(decoded_auth_header)
        if user_credentials is None:
            return None
        user = self.user_object_from_credentials(user_credentials[0],
                                                 user_credentials[1])
        return user
