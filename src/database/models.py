from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Contact(Base):
    __tablename__ = 'contacts'

    id = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String)
    phone_number = Column(String)
    birthday = Column(Date)
    additional_data = Column(String)

    def __repr__(self):
        return f"<Contact(first_name='{self.first_name}', last_name='{self.last_name}', email='{self.email}', phone_number='{self.phone_number}', birthday='{self.birthday}', additional_data='{self.additional_data}')>"
