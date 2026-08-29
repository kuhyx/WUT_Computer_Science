#!/usr/bin/env python3
"""The two persisted tables: an account, and one account's score for one film.

Split out of `app.py`, which went over this repo's 250-line cap when the models
were migrated to SQLAlchemy 2.0's typed declarative style. They import nothing
from `app`, so there is no cycle: `app.py` builds the `SQLAlchemy` object from
`Base` rather than the models being built from it.
"""

from __future__ import annotations

from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    """Declarative base for this app's two models.

    `class User(db.Model)` was attribute access, which mypy cannot resolve in a
    base-class position -- that was four `--strict` errors. A named base fixes
    it. The trade is that flask-sqlalchemy's `Model` mixin goes with it, so
    table names are spelled out here rather than derived from the class name.
    """


class User(Base):
    """One Firebase account, remembered so ratings have an owner."""

    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)
    uid: Mapped[str] = mapped_column(String(80), unique=True)
    email: Mapped[str] = mapped_column(String(80), unique=True)
    # Nullable with a default, exactly as the submitted schema had it.
    is_admin: Mapped[bool | None] = mapped_column(default=False)


class Rating(Base):
    """One user's score for one film."""

    __tablename__ = "rating"

    id: Mapped[int] = mapped_column(primary_key=True)
    # As handed in: the foreign key points at user.uid (a VARCHAR) while the
    # column itself is declared INTEGER, and what actually gets stored is the
    # Firebase uid string -- SQLite is dynamically typed, so this worked. The
    # explicit Integer keeps the submitted DDL byte-identical, because
    # mapped_column otherwise infers VARCHAR(80) from the referenced column;
    # the `str` annotation is what the code really puts in it.
    user_id: Mapped[str] = mapped_column(Integer, ForeignKey("user.uid"))
    movie_id: Mapped[int]
    value: Mapped[int]
