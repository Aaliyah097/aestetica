import datetime

from sqlalchemy import (
    String, Float, Boolean, Integer, select,
    ForeignKey, create_engine, update, Table,
    Column, DateTime
)
from typing import List, Optional
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Session
from . import config

engine = create_engine(
    config.DB_URL,
    echo=True
)


class Base(DeclarativeBase):
    session = None

    def __enter__(self):
        self.session = Session(engine)
        return self.session

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            if exc_type or exc_val:
                self.session.rollback()
                raise Exception("Rollback %s, %s, %s" % (str(exc_type), str(exc_val), str(exc_tb)))
            else:
                self.session.rollback()
            self.session.close()
            self.session = None


class Staff(Base):
    __tablename__ = "staff"

    name: Mapped[str] = mapped_column(String(150), unique=True, primary_key=True, autoincrement=False)
    role: Mapped[str] = mapped_column(ForeignKey("roles.name"))
    is_new: Mapped[bool] = mapped_column(Boolean(), default=False)


class Role(Base):
    __tablename__ = 'roles'
    
    name: Mapped[str] = mapped_column(String(150), primary_key=True, unique=True, autoincrement=False)


class Filial(Base):
    __tablename__ = 'filials'

    name: Mapped[str] = mapped_column(String(50), primary_key=True, unique=True, autoincrement=False)
    db_address: Mapped[str] = mapped_column(String(15), nullable=True)
    db_port: Mapped[str] = mapped_column(String(5), nullable=True)
    db_name: Mapped[str] = mapped_column(String(50), nullable=True)
    db_user: Mapped[str] = mapped_column(String(150), nullable=True)
    db_password: Mapped[str] = mapped_column(String(150), nullable=True)


class Department(Base):
    __tablename__ = 'departments'

    name: Mapped[str] = mapped_column(String(50), primary_key=True, unique=True, autoincrement=False)


class Salary(Base):
    __tablename__ = 'salary'

    id: Mapped[int] = mapped_column(Integer(), primary_key=True, unique=True, autoincrement=True)
    staff: Mapped[str] = mapped_column((ForeignKey('staff.name')))
    department: Mapped[str] = mapped_column(ForeignKey('departments.name'))
    fix: Mapped[float] = mapped_column(Float(), default=0, nullable=False)


class SalaryGrid(Base):
    __tablename__ = 'salary_grid'

    id: Mapped[int] = mapped_column(Integer(), primary_key=True, unique=True, autoincrement=True)
    salary: Mapped[int] = mapped_column(ForeignKey('salary.id'))
    limit: Mapped[float] = mapped_column(Float())
    percent: Mapped[float] = mapped_column(Float())


class Service(Base):
    __tablename__ = 'services'

    code: Mapped[str] = mapped_column(String(20), primary_key=True, unique=True, autoincrement=False)
    name: Mapped[str] = mapped_column(String(500))


class Consumables(Base):
    __tablename__ = 'consumables'

    id: Mapped[int] = mapped_column(Integer(), primary_key=True, unique=True, autoincrement=True)
    service: Mapped[str] = mapped_column(ForeignKey('services.code'))
    staff: Mapped[str] = mapped_column(ForeignKey('staff.name'))
    cost: Mapped[float] = mapped_column(Float(), default=0, nullable=False)
