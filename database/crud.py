'''This module defines general database CRUD operations.'''

from typing import Any
from fastapi import status
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from helpers.api_exceptions import ResponseValidationError


def get_object(
    db: Session,
    table: object,
    column: object,
    value: Any,
    exc_status_code: status = status.HTTP_409_CONFLICT,
    exc_message: str = 'Unable to find object in the database.'
):
    '''
    Fetch database object that matches 1 condition, if exists.

        :param db [generator]: Database session.
        :param table [orm]: Declarative base Table.
        :param column [orm]: Declarative base Column.
        :param value: Value to look up.
        :param exc_status_code [int]: Exception HTTP status code.
        :param exc_message [str]: Exception error message.

        :returns: Database object.
    '''
    try:
        data = db.query(table).filter(column == value).first()
        if not data:
            raise ResponseValidationError(
                status_code=exc_status_code,
                message=exc_message
            )
        return data

    except SQLAlchemyError as e:
        raise ResponseValidationError(
            status_code=exc_status_code,
            message=exc_message) from e

    finally:
        db.close()


def get_table(
    db: Session,
    table: object,
    exc_status_code: status = status.HTTP_409_CONFLICT,
    exc_message: str = 'Unable to find table in the database.'
):
    '''
    Fetch all database objects from a table.

        :param db [generator]: Database session.
        :param table [orm]: Declarative base Table.
        :param exc_status_code [int]: Exception HTTP status code.
        :param exc_message [str]: Exception error message.

        :returns: Database table objects.
    '''
    try:
        data = db.query(table).all()
        if not data:
            raise ResponseValidationError(
                status_code=exc_status_code,
                message=exc_message
            )
        return data

    except SQLAlchemyError as e:
        raise ResponseValidationError(
            status_code=exc_status_code,
            message=exc_message) from e

    finally:
        db.close()


def create_object(
    db: Session,
    data: object,
    exc_status_code: status = status.HTTP_409_CONFLICT,
    exc_message: str = 'Unable to add object to the database.'
):
    '''
    Add an object to the database.

        :param db [generator]: Database session.
        :param data [orm]: Declarative base object.
        :param exc_status_code [int]: Exception HTTP status code.
        :param exc_message [str]: Exception error message.
    '''
    try:
        db.add(data)
        db.commit()

    except SQLAlchemyError as e:
        db.rollback()
        raise ResponseValidationError(
            status_code=exc_status_code,
            message=exc_message) from e

    finally:
        db.close()


def create_objects(
    db: Session,
    data: list,
    exc_status_code: status = status.HTTP_409_CONFLICT,
    exc_message: str = 'Unable to add objects to the database.'
):
    '''
    Add multiple objects to the database.

        :param db [generator]: Database session.
        :param data [list[[orm]]: List of declarative base objects.
        :param exc_status_code [int]: Exception HTTP status code.
        :param exc_message [str]: Exception error message.
    '''
    try:
        db.add_all(data)
        db.commit()

    except SQLAlchemyError as e:
        db.rollback()
        raise ResponseValidationError(
            status_code=exc_status_code,
            message=exc_message) from e

    finally:
        db.close()


def update_object(
    db: Session,
    table: object,
    column: object,
    value: Any,
    data: dict,
    exc_status_code: status = status.HTTP_409_CONFLICT,
    exc_message: str = 'Unable to update object in the database.'
):
    '''
    Update a database object.

        :param db [generator]: Database session.
        :param table [orm]: Declarative base Table.
        :param column [orm]: Declarative base Column.
        :param value: Value to look up.
        :param data [dict]: Update dictionary.
        :param exc_status_code [int]: Exception HTTP status code.
        :param exc_message [str]: Exception error message.
    '''

    try:
        db.query(table).filter(column == value).update(data)
        db.commit()

    except SQLAlchemyError as e:
        db.rollback()
        raise ResponseValidationError(
            status_code=exc_status_code,
            message=exc_message) from e

    finally:
        db.close()


def delete_object(
    db: Session,
    data: object,
    exc_status_code: status = status.HTTP_409_CONFLICT,
    exc_message: str = 'Unable to delete object from the database.'
):
    '''
    Delete a database object.

        :param db [generator]: Database session.
        :param data [orm]: Declarative base object.
        :param exc_status_code [int]: Exception HTTP status code.
        :param exc_message [str]: Exception error message.
    '''
    try:
        db.delete(data)
        db.commit()

    except SQLAlchemyError as e:
        db.rollback()
        raise ResponseValidationError(
            status_code=exc_status_code,
            message=exc_message) from e

    finally:
        db.close()
