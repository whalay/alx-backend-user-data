#!/usr/bin/env python3
""" This module contains an auth class """
import re
from flask import request
from typing import List, TypeVar


class Auth:
    """ manages api authentication """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ a require auth function """
        if path is None or not excluded_paths:
            return True

        if not path.endswith('/'):
            path_comp = path + '/'
        else:
            path_comp = path

        for excluded_path in excluded_paths:
            if re.match(excluded_path.replace('*', '.*'), path_comp):
                return False

        return True

    def authorization_header(self, request=None) -> str:
        """ an authorization header function """
        if request is None:
            return None

        return request.headers.get('Authorization')

    def current_user(self, request=None) -> TypeVar('User'):
        """ a current user function """
        return None
