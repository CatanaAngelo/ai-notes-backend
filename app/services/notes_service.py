from sqlalchemy.orm import Session
from sqlalchemy import or_
from fastapi import HTTPException

from app.models import Note, User
from app.schemas import NoteCreate
from app.ai_client import summarize

import logging

logger = logging.getLogger(__name__)

def get_notes(db: Session, user: User, limit: int, offset: int, query: str | None = None):
    q = db.query(Note).filter(Note.user_id == user.id)

    if query:
        q = q.filter(
            or_(
                Note.title.ilike(f"%{query}%"),
                Note.content.ilike(f"%{query}%")
            )
        )

    return (
        q.order_by(Note.created_at.desc())
        .offset(offset)
        .limit(limit)
        .all()
    )

def create_note(db: Session, user: User, new_note: NoteCreate):
    note = Note(
        title=new_note.title,
        content=new_note.content,
        user_id=user.id # am adaugat user ca sa nu poata oricine face orice
        )

    db.add(note)
    db.commit()
    db.refresh(note)
    
    logger.info("Note created!", extra={"note_id": note.id, "user_id": user.id})
    return note


def get_note(db: Session, user: User, note_id: int):
    note = db.query(Note).filter(
        Note.id == note_id,
        Note.user_id == user.id
    ).first()

    if note is None:
        logger.warning("Note not found!", extra={"note_id": note_id, "user_id": user.id})
        raise HTTPException(status_code=404, detail="Note not found")
    
    logger.info("Note found!", extra={"note_id": note.id, "user_id": user.id})
    return note


def update_note(db: Session, user: User, note_id: int, new_note: NoteCreate):
    note = db.query(Note).filter(
        Note.id == note_id,
        Note.user_id == user.id
    ).first()

    if note is None:
        logger.warning("Note not found!", extra={"note_id": note_id, "user_id": user.id})
        raise HTTPException(status_code=404, detail="Note not found")
    
    note.title = new_note.title
    note.content = new_note.content

    db.commit()
    db.refresh(note)

    logger.info("Note updated!", extra={"note_id": note.id, "user_id": user.id})
    return note


def delete_note(db: Session, user: User, note_id: int):
    note = db.query(Note).filter(
        Note.id == note_id,
        Note.user_id == user.id
    ).first()

    if note is None:
        logger.warning("Note not found!", extra={"note_id": note_id, "user_id": user.id})
        raise HTTPException(status_code=404, detail="Note not found")

    db.delete(note)
    db.commit()

    logger.info("Note deleted!", extra={"note_id": note.id, "user_id": user.id})
    return note


def summarize_note(db: Session, user: User, note_id: int):
    note = db.query(Note). filter(
        Note.id == note_id,
        Note.user_id == user.id
    ).first()

    if not note:
        logger.warning("Note not found!", extra={"note_id": note_id, "user_id": user.id})
        raise HTTPException(status_code=404, detail="Note not found")
    
    summary = summarize(note.content)

    logger.info("Note summarized successfully", extra={"note_id": note.id, "user_id": user.id})
    return {
        "note_id": note.id,
        "summary": summary,
        "original_length": len(note.content)
    }