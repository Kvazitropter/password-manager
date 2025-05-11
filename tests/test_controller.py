import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from unittest.mock import MagicMock, patch

import pytest
from psycopg2 import ProgrammingError

from backend.controller import Controller
from backend.custom_errors import (
    ConnectionError,
    ExistingAccount,
    ExistingEntry,
    IncorrectMasterKey,
    NonExistingAccount,
)


@pytest.fixture
def mock_repo():
    return MagicMock()


@pytest.fixture
def controller(mock_repo):
    return Controller(mock_repo)


def test_is_existing_account_true(controller, mock_repo):
    mock_repo.has_account_query.return_value = True
    assert controller.is_existing_account('test_user')
    mock_repo.has_account_query.assert_called_once_with('test_user')


def test_is_existing_account_false(controller, mock_repo):
    mock_repo.has_account_query.return_value = False
    assert not controller.is_existing_account('test_user')


def test_login_success(controller, mock_repo):
    mock_repo.has_account_query.return_value = True
    mock_repo.get_memory_mk_and_salt_query.return_value = (
        b'encrypted_data', b'salt'
    )

    with patch('backend.controller.decrypt', return_value='control'):
        controller.login('test_user', 'master_key')

    mock_repo.has_account_query.assert_called_once_with('test_user')
    mock_repo.get_memory_mk_and_salt_query.assert_called_once_with('test_user')


def test_login_non_existing_account(controller, mock_repo):
    mock_repo.has_account_query.return_value = False

    with pytest.raises(NonExistingAccount):
        controller.login('test_user', 'master_key')


def test_login_incorrect_master_key(controller, mock_repo):
    mock_repo.has_account_query.return_value = True
    mock_repo.get_memory_mk_and_salt_query.return_value = (
        b'encrypted_data', b'salt'
    )

    with patch('backend.controller.decrypt', side_effect=Exception):
        with pytest.raises(IncorrectMasterKey):
            controller.login('test_user', 'wrong_key')


def test_create_new_account_success(controller, mock_repo):
    mock_repo.has_account_query.return_value = False
    with patch('backend.controller.encrypt', return_value=(b'encrypted', b'salt')):
        controller.create_new_account('new_user', 'master_key')
    
    mock_repo.has_account_query.assert_called_once_with('new_user')
    mock_repo.add_new_account_query.assert_called_once_with(
        'new_user', b'encrypted', b'salt'
    )


def test_create_new_account_existing(controller, mock_repo):
    mock_repo.has_account_query.return_value = True

    with pytest.raises(ExistingAccount):
        controller.create_new_account('existing_user', 'master_key')


def test_get_entries(controller, mock_repo):
    expected = [(1, 's_name', 'login')]
    mock_repo.get_all_entries_query.return_value = expected
    result = controller.get_entries('test_user')

    assert result == expected
    mock_repo.get_all_entries_query.assert_called_once_with('test_user')


def test_get_entry_password(controller, mock_repo):
    mock_repo.get_entry_password_query.return_value = (
        memoryview(b'encrypted'),
        memoryview(b'salt')
    )
    with patch('backend.controller.decrypt', return_value='decrypted'):
        result = controller.get_entry_password(1, 'master_key')
        assert result == 'decrypted'

    mock_repo.get_entry_password_query.assert_called_once_with(1)


def test_is_existing_entry_true(controller, mock_repo):
    mock_repo.has_entry_query.return_value = True
    assert controller.is_existing_entry('user_login', 's_name', 'login')
    mock_repo.has_entry_query.assert_called_once_with(
        'user_login', 's_name', 'login'
    )


def test_is_existing_entry_false(controller, mock_repo):
    mock_repo.has_entry_query.return_value = False
    assert not controller.is_existing_entry('user_login', 's_name', 'login')


def test_add_new_entry_success(controller, mock_repo):
    mock_repo.has_entry_query.return_value = False
    with patch('backend.controller.encrypt', return_value=(b'encrypted', b'salt')):
        controller.add_new_entry(
            'user_login', 'master_key', 's_name', 'login', 'password'
        )
    
    mock_repo.has_entry_query.assert_called_once_with(
        'user_login', 's_name', 'login'
    )
    mock_repo.add_new_entry_query.assert_called_once_with(
        'user_login', 's_name', 'login', b'encrypted', b'salt'
    )


def test_add_new_entry_existing(controller, mock_repo):
    mock_repo.has_entry_query.return_value = True

    with pytest.raises(ExistingEntry):
        controller.add_new_entry(
            'user_login', 'master_key', 's_name', 'login', 'password'
        )


def test_update_entry(controller, mock_repo):
    with patch('backend.controller.encrypt', return_value=(b'encrypted', b'salt')):
        controller.update_entry('master_key', 1, 'new_password')
    
    mock_repo.update_entry_query.assert_called_once_with(
        1, b'encrypted', b'salt'
    )


def test_update_non_existing_entry(controller, mock_repo):
    mock_repo.update_entry_query.side_effect = ProgrammingError
    with patch('backend.controller.encrypt', return_value=(b'encrypted', b'salt')):
        with pytest.raises(ProgrammingError):
            controller.update_entry('master_key', 1, 'new_password')


def test_delete_entry(controller, mock_repo):
    controller.delete_entry(1)
    mock_repo.delete_entry_query.assert_called_once_with(1)


def test_delete_nonexistent_entry(controller, mock_repo):
    mock_repo.delete_entry_query.return_value = None
    controller.delete_entry(999)


def test_no_connection(controller, mock_repo):
    mock_repo.has_account_query.side_effect = ConnectionError

    with pytest.raises(ConnectionError):
        controller.is_existing_account('test_user')

    with pytest.raises(ConnectionError):
        controller.login('test_user', 'master_key')

    with pytest.raises(ConnectionError):
        controller.create_new_account('test_user', 'master_key')
        

def test_no_connection_memory_mk_and_salt(controller, mock_repo):
    mock_repo.get_memory_mk_and_salt_query.side_effect = ConnectionError
    
    with pytest.raises(ConnectionError):
        controller.login('test_user', 'master_key')


def test_no_connection_add_new_account_query(controller, mock_repo):
    mock_repo.has_account_query.return_value = False
    mock_repo.add_new_account_query.side_effect = ConnectionError
    
    with pytest.raises(ConnectionError):
        controller.create_new_account('test_user', 'master_key')


def test_no_connection_get_all_entries_query(controller, mock_repo):
    mock_repo.get_all_entries_query.side_effect = ConnectionError
    
    with pytest.raises(ConnectionError):
        controller.get_entries('test_user')


def test_no_connection_get_entry_password_query(controller, mock_repo):
    mock_repo.get_entry_password_query.side_effect = ConnectionError
    
    with pytest.raises(ConnectionError):
        controller.get_entry_password(1, 'master_key')


def test_no_connection_has_entry_query(controller, mock_repo):
    mock_repo.has_entry_query.side_effect = ConnectionError
    
    with pytest.raises(ConnectionError):
        controller.is_existing_entry('user_login', 's_name', 'login')
        
    with pytest.raises(ConnectionError):
        controller.add_new_entry(
            'user_login', 'master_key', 's_name', 'login', 'password'
        )


def test_no_connection_add_new_entry_query(controller, mock_repo):
    mock_repo.has_entry_query.return_value = False
    mock_repo.add_new_entry_query.side_effect = ConnectionError
    
    with pytest.raises(ConnectionError):
        controller.add_new_entry(
            'user_login', 'master_key', 's_name', 'login', 'password'
        )


def test_no_connection_update_entry_query(controller, mock_repo):
    mock_repo.update_entry_query.side_effect = ConnectionError
    
    with pytest.raises(ConnectionError):
        controller.update_entry('user_login', 1, 'password')


def test_no_connection_delete_entry_query(controller, mock_repo):
    mock_repo.delete_entry_query.side_effect = ConnectionError
    
    with pytest.raises(ConnectionError):
        controller.delete_entry(1)