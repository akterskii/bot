import dataclasses
from dataclasses import asdict

import pytest

from main_logic.common.common_const import USERS_COLLECTION
from main_logic.user_managment.users_crud import DatastoreClient, User


def test_singleton():
    client1 = DatastoreClient().get_client()
    client2 = DatastoreClient().get_client()
    assert client1 == client2


def test_get_user():
    user = User.get_user_by_telegram_id(telegram_id='tgid1')
    assert user, 'User with all fields was not set properly'
    user = User.get_user_by_telegram_id(telegram_id='tgid2')
    assert user, 'User without web credentials was not set properly'


def test_from_dict():
    web_dict = {
        'user_name': 'u1',
        'email': 'e1',
        'password_hash': 'ph1',
        'registration_date': '2020.02.12 12:11:01'
    }
    user_dict = {
        'user_id': "id1",
        'first_name': "aa",
        'last_name': "bb",
        'telegram_id': 'tgid_1',
        'web_credentials': web_dict
    }
    user = User(**user_dict)

    assert asdict(user) == user_dict


def test_update():
    tmp_first_name = "Aa"
    # get doc
    user = User.get_user_by_telegram_id(telegram_id='tgid1')
    real_first_name = user.first_name
    # update the doc
    user.first_name = tmp_first_name
    user.update_db()
    # upload updated version
    user = User.get_user_by_telegram_id(telegram_id='tgid1')
    assert user.first_name == tmp_first_name
    # restore initial value
    user.first_name = real_first_name
    user.update_db()


def test_delete_and_add():
    u = User(
        user_id='',
        first_name='aa',
        last_name='bb',
        telegram_id='cc'
    )
    u.add_to_db()
    print(u.user_id)
    assert DatastoreClient().get_client().collection(USERS_COLLECTION).document(u.user_id)