#!/usr/bin/env python3
""" Main file for tests """
import requests


def register_user(email: str, password: str) -> None:
    """ tests the register users endpoint """
    res = requests.post('http://localhost:5000/users',
                        data={'email': email, 'password': password})
    res_data = res.json()

    assert res.status_code == 200
    assert type(res_data) is dict
    assert len(res_data.keys()) == 2
    assert 'email' in res_data
    assert 'message' in res_data
    assert res_data['email'] == email
    assert res_data['message'] == 'user created'

    res = requests.post('http://localhost:5000/users',
                        data={'email': email, 'password': password})
    res_data = res.json()

    assert res.status_code == 400
    assert type(res_data) is dict
    assert len(res_data.keys()) == 1
    assert 'email' not in res_data
    assert 'message' in res_data
    assert res_data['message'] == 'email already registered'


def log_in_wrong_password(email: str, password: str) -> None:
    """ test the login route with wrong password """
    res = requests.post('http://localhost:5000/sessions',
                        data={'email': email, 'password': password})

    assert res.status_code == 401


def log_in(email: str, password: str) -> str:
    """ test the login with correct credentials """
    res = requests.post('http://localhost:5000/sessions',
                        data={'email': email, 'password': password})
    cookies = res.cookies
    res_data = res.json()

    assert res.status_code == 200
    assert type(res_data) is dict
    assert len(res_data.keys()) == 2
    assert 'email' in res_data
    assert 'message' in res_data
    assert res_data['email'] == email
    assert res_data['message'] == 'logged in'
    assert 'session_id' in cookies

    return cookies.get('session_id')


def profile_unlogged() -> None:
    """ test the profile when not logged in """
    res = requests.get('http://localhost:5000/profile')

    assert res.status_code == 403


def profile_logged(session_id: str) -> None:
    """ test the profile a user is logged in """
    res = requests.get('http://localhost:5000/profile',
                       cookies={'session_id': session_id})
    res_data = res.json()

    assert res.status_code == 200
    assert type(res_data) is dict
    assert len(res_data.keys()) == 1
    assert 'email' in res_data


def log_out(session_id: str) -> None:
    """ test the logout route """
    res = requests.delete('http://localhost:5000/sessions',
                          cookies={'session_id': session_id})

    assert res.status_code == 200


def reset_password_token(email: str) -> str:
    """ test the reset password token route """
    res = requests.post('http://localhost:5000/reset_password',
                        data={'email': email})
    res_data = res.json()

    assert res.status_code == 200
    assert type(res_data) is dict
    assert len(res_data.keys()) == 2
    assert 'email' in res_data
    assert 'reset_token' in res_data
    assert res_data['email'] == email

    return res_data['reset_token']


def update_password(email: str, reset_token: str, new_password: str) -> None:
    """ test the update password route """
    res = requests.put('http://localhost:5000/reset_password',
                       data={'email': email,
                             'reset_token': reset_token,
                             'new_password': new_password})
    res_data = res.json()

    assert res.status_code == 200
    assert type(res_data) is dict
    assert len(res_data.keys()) == 2
    assert 'email' in res_data
    assert 'message' in res_data
    assert res_data['email'] == email
    assert res_data['message'] == 'Password updated'


EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"


if __name__ == "__main__":

    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
