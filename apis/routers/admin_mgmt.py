'''This module is part of the /admin FastAPI router.'''

from fastapi import APIRouter, Depends, status
from fastapi_pagination import Page, paginate
from sqlalchemy.orm import Session

from apis.schemas.admin import CreateAdminRequest, UpdateAdminRequest, RetrieveAdminsResponse, CreateAdminResponse, UpdateAdminResponse
from database import crud, models
from database.session import get_db
from security.admin import get_current_active_admin
from security.hashing import SecureHash


router = APIRouter(dependencies=[Depends(get_current_active_admin)])


@router.get('', status_code=status.HTTP_200_OK, response_model=Page[RetrieveAdminsResponse])
async def retrieve_admins(
    db: Session = Depends(get_db)
):
    '''
    Retrieve admins from the database.

        :returns [RetrieveAdminsResponse]: Admin accounts.
    '''

    # get admin from the database
    admin_objects = crud.get_table(
        db=db,
        table=models.AdminsTable,
        exc_message='Unable to find admins.'
    )

    return paginate([item.__dict__ for item in admin_objects])


@router.post('/create', status_code=status.HTTP_200_OK, response_model=CreateAdminResponse)
async def add_admin(
    item: CreateAdminRequest,
    db: Session = Depends(get_db)
):
    '''
    Add new admin in the database.

        :param username [str]: New admin username.
        :param password [str]: New admin password.

        :returns [CreateAdminResponse]: Admin account that has just been created.
    '''

    # create database new admin object
    admin_object = models.AdminsTable(
        username=item.username,
        hashed_password=SecureHash.create(item.password),
        is_active=True
    )

    # add new admin to the database
    crud.create_object(
        db=db,
        object=admin_object,
        exc_message='Unable to create admin.'
    )

    new_admin = crud.get_object(
        db=db,
        table=models.AdminsTable,
        column=models.AdminsTable.username,
        value=item.username,
        exc_message='Unable to find admin.'
    )

    return new_admin.__dict__


@router.post('/update', status_code=status.HTTP_200_OK, response_model=UpdateAdminResponse)
async def alter_admin_status(
    item: UpdateAdminRequest,
    db: Session = Depends(get_db)
):
    '''
    Update other admin status (is_active) in the database.

        :param username [str]: Other admin username.
        :param is_active [bool]: Other admin status.

        :returns [UpdateAdminResponse]: Admin account that has just been updated.
    '''

    # update other admin in the database
    crud.update_object(
        db=db,
        table=models.AdminsTable,
        column=models.AdminsTable.username,
        value=item.username,
        object=dict(is_active=item.is_active),
        exc_message='Unable to update admin.'
    )

    updated_admin = crud.get_object(
        db=db,
        table=models.AdminsTable,
        column=models.AdminsTable.username,
        value=item.username,
        exc_message='Unable to find admin.'
    )

    return updated_admin.__dict__
