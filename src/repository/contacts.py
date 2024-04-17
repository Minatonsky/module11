from typing import List
from datetime import date, timedelta

from sqlalchemy.orm import Session
from sqlalchemy import or_, and_
from sqlalchemy import extract

from src.database.models import Contact, User
from src.schemas import ContactCreate


async def get_contacts(skip: int, limit: int, user: User, db: Session) -> List[Contact]:
    return db.query(Contact).filter(Contact.user_id == user.id).offset(skip).limit(limit).all()


async def get_contact(contact_id: int, user: User, db: Session) -> Contact:
    return db.query(Contact).filter(and_(Contact.user_id == user.id, Contact.id == contact_id)).first()


async def create_contact(body: ContactCreate, user: User, db: Session) -> Contact:
    contact = Contact(**body.dict(), user_id=user.id)
    db.add(contact)
    db.commit()
    db.refresh(contact)
    return contact


async def update_contact(contact_id: int, body: ContactCreate, user: User, db: Session) -> Contact | None:
    contact = db.query(Contact).filter(and_(Contact.id == contact_id, Contact.user_id == user.id)).first()
    if contact:
        for field, value in body.dict().items():
            setattr(contact, field, value)
        db.commit()
    return contact


async def remove_contact(contact_id: int, user: User, db: Session) -> Contact | None:
    contact = db.query(Contact).filter(and_(Contact.id == contact_id, Contact.user_id == user.id)).first()
    if contact:
        db.delete(contact)
        db.commit()
    return contact


async def search_contacts(query: str, user: User, db: Session) -> List[Contact]:
    return db.query(Contact).filter(
        and_(Contact.user_id == user.id,
        or_(
            Contact.first_name.ilike(f"%{query}%"),
            Contact.last_name.ilike(f"%{query}%"),
            Contact.email.ilike(f"%{query}%")
        ))
    ).all()


async def get_contacts_by_birthdays(user: User, db: Session) -> List[Contact]:
    today = date.today()
    end_date = today + timedelta(days=7)
    contacts = db.query(Contact).filter(
        and_(Contact.user_id == user.id,
        extract('month', Contact.birthday) == today.month,
        extract('day', Contact.birthday) >= today.day,
        extract('day', Contact.birthday) <= end_date.day
    )).all()
    return contacts
