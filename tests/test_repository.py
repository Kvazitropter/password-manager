from unittest.mock import MagicMock, patch

import pytest
from psycopg2 import OperationalError

from backend.custom_errors import ConnectionError
from backend.repository import Repository


@pytest.fixture
def mock_conn():
    return MagicMock()


@pytest.fixture
def mock_cursor(mock_conn):
    cursor = MagicMock()
    mock_conn.cursor.return_value = cursor
    return cursor


@pytest.fixture
def repository(mock_conn):
    with patch('psycopg2.connect', return_value=mock_conn) as mock_connect:
        repository = Repository()
        yield repository
        mock_connect.assert_called()


def test_has_account_query_true(repository, mock_cursor):
    mock_cursor.fetchone.return_value = (True,)

    assert repository.has_account_query('test_user')
    mock_cursor.execute.assert_called_once_with(
        'SELECT EXISTS(SELECT 1 FROM "user" WHERE login = (%s))',
        ('test_user',)
    )


def test_get_memory_mk_and_salt_query(repository, mock_cursor):
    expected = (b'encrypted', b'salt')
    mock_cursor.fetchone.return_value = expected
    result = repository.get_memory_mk_and_salt_query('test_user')

    assert result == expected
    mock_cursor.execute.assert_called_once_with(
        'SELECT encrypted_control_string, salt FROM "user" WHERE login = (%s)',
        ('test_user',)
    )


def test_add_new_account_query(repository, mock_conn, mock_cursor):
    repository.add_new_account_query('new_user', b'encrypted', b'salt')
    mock_cursor.execute.assert_called_once_with(
        'INSERT INTO "user" (login, encrypted_control_string, '
        'salt) '
        'VALUES (%s, %s, %s)',
        ('new_user', b'encrypted', b'salt')
    )
    mock_conn.commit.assert_called_once()
    

def test_get_all_entries_query(repository, mock_cursor):
    expected = [(1, 's_name1', 'login1'), (2, 's_name2', 'login2')]
    mock_cursor.fetchall.return_value = expected
    result = repository.get_all_entries_query('test_user')

    assert result == expected
    mock_cursor.execute.assert_called_once_with(
        'SELECT id, service_name, login FROM account WHERE user_login = %s',
        ('test_user',)
    )


def test_get_entry_password_query(repository, mock_cursor):
    expected = (b'encrypted', b'salt')
    mock_cursor.fetchone.return_value = expected
    result = repository.get_entry_password_query(1)

    assert result == expected
    mock_cursor.execute.assert_called_once_with(
        'SELECT encrypted_password, salt FROM account WHERE id = %s',
        (1,)
    )


def test_has_entry_query(repository, mock_cursor):
    mock_cursor.fetchone.return_value = (True,)

    assert repository.has_entry_query('test_user', 's_name', 'login')
    mock_cursor.execute.assert_called_once_with(
        'SELECT EXISTS(SELECT 1 FROM account '
        'WHERE (user_login, service_name, login) = (%s, %s, %s))',
        ('test_user', 's_name', 'login')
    )


def test_add_new_entry_query(repository, mock_conn, mock_cursor):
    repository.add_new_entry_query(
        'user_login', 's_name', 'login', b'encrypted', b'salt'
    )
    mock_cursor.execute.assert_called_once_with(
        'INSERT INTO account (user_login, service_name, login, '
        'encrypted_password, salt) '
        'VALUES (%s, %s, %s, %s, %s)',
        ('user_login', 's_name', 'login', b'encrypted', b'salt')
    )
    mock_conn.commit.assert_called_once()


def test_update_entry_query(repository, mock_conn, mock_cursor):
    repository.update_entry_query(1, b'encrypted', b'salt')
    mock_cursor.execute.assert_called_once_with(
        'UPDATE account SET (encrypted_password, salt) = (%s, %s) WHERE id = (%s)',
        (b'encrypted', b'salt', 1)
    )
    mock_conn.commit.assert_called_once()


def test_delete_entry_query(repository, mock_conn, mock_cursor):
    repository.delete_entry_query(1)
    mock_cursor.execute.assert_called_once_with(
        'DELETE FROM account WHERE id = %s',
        (1,)
    )
    mock_conn.commit.assert_called_once()


def test_no_connection():
    with patch('psycopg2.connect', side_effect=OperationalError('No connection')):
        repository = Repository()
        with pytest.raises(ConnectionError):
            repository.has_account_query('test_user')