#!/usr/bin/env python3
""" A basic authentication class """
import base64
from api.v1.auth.auth import Auth
from models.user import User
from typing import TypeVar


class SessionAuth(Auth):
    """ a session auth class """
