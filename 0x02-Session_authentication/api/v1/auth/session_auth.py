#!/usr/bin/env python3
""" A basic authentication class """
import base64
from api.v1.auth.auth import Auth
from models.user import User
from typing import TypeVar
import uuid
from flask import request


class SessionAuth(Auth):
    """ a session auth class """
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """Create a Session ID for a user_id."""
        if not user_id or not isinstance(user_id, str):
            return None
        session_id = str(uuid.uuid4())
        self.user_id_by_session_id[session_id] = user_id
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        '''self descriptive'''
        if session_id and isinstance(session_id, str):
            return self.user_id_by_session_id.get(session_id)
        return None

    def current_user(self, request=None):
        '''self descriptive'''
        session_cookie = self.session_cookie(request)
        session_id = self.user_id_for_session_id(session_cookie)
        user = User.get(session_id)
        return user

    def destroy_session(self, request=None):
        '''self descriptive'''
        if not request:
            return False
        session_cookie = self.session_cookie(request)

        if not session_cookie:
            return False

        user_id = self.user_id_for_session_id(session_cookie)

        if not user_id:
            return False
        self.user_id_by_session_id.pop(session_cookie)
        return True
