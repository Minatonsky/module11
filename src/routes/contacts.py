from typing import List

from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, status

from src.database.db import get_db
from src.database.models import User
from src.schemas import ContactCreate, Contact
from src.repository import contacts as repository_contacts
from src.services.auth import auth_service

router = APIRouter(prefix='/contacts', tags=["contacts"])


@router.get("/", response_model=List[Contact])
async def read_contacts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db),
                        current_user: User = Depends(auth_service.get_current_user)):
    contacts = await repository_contacts.get_contacts(skip, limit, current_user, db)
    return contacts


@router.get("/{contact_id}", response_model=Contact)
async def read_contact(contact_id: int, db: Session = Depends(get_db),
                       current_user: User = Depends(auth_service.get_current_user)):
    contact = await repository_contacts.get_contact(contact_id, current_user, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return contact


@router.post("/", response_model=Contact, status_code=status.HTTP_201_CREATED)
async def create_contact(body: ContactCreate, db: Session = Depends(get_db),
                         current_user: User = Depends(auth_service.get_current_user)):
    return await repository_contacts.create_contact(body, current_user, db)


@router.put("/{contact_id}", response_model=Contact)
async def update_contact(body: ContactCreate, contact_id: int, db: Session = Depends(get_db),
                         current_user: User = Depends(auth_service.get_current_user)):
    contact = await repository_contacts.update_contact(contact_id, body, current_user, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return contact


@router.delete("/{contact_id}", response_model=Contact)
async def remove_contact(contact_id: int, db: Session = Depends(get_db),
                         current_user: User = Depends(auth_service.get_current_user)):
    contact = await repository_contacts.remove_contact(contact_id, current_user, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return contact


@router.get("/search/", response_model=List[Contact])
async def search_contacts(query: str, db: Session = Depends(get_db),
                          current_user: User = Depends(auth_service.get_current_user)):
    contacts = await repository_contacts.search_contacts(query, current_user, db)
    return contacts


@router.get("/upcoming-birthdays/", response_model=List[Contact])
async def get_upcoming_birthdays(db: Session = Depends(get_db),
                                 current_user: User = Depends(auth_service.get_current_user)):
    return await repository_contacts.get_contacts_by_birthdays(current_user, db)