from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.db import get_db
from app.schemas import NoteCreate, NoteResponse, NoteSummaryResponse
from app.services import notes_service
from app.security import get_current_user
from app.models import User

from typing import Optional

router = APIRouter()

@router.get("/notes/", response_model=list[NoteResponse])
def get_notes(
    limit: int = Query(default=10, ge=1),
    offset: int = Query(default=0, ge=0),
    query: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return notes_service.get_notes(db, current_user, limit, offset, query)

@router.post("/notes/", response_model=NoteResponse, status_code=201)
def add_new_note(
    new_note: NoteCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return notes_service.create_note(db, current_user, new_note)

@router.get("/notes/{note_id}", response_model=NoteResponse)
def get_single_note(
    note_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
                    
):
    return notes_service.get_note(db, current_user, note_id)

@router.put("/notes/{note_id}", response_model=NoteResponse)
def update_note(
    note_id: int,
    new_note: NoteCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return notes_service.update_note(db, current_user, note_id, new_note)

@router.delete("/notes/{note_id}", response_model=NoteResponse)
def delete_note(
    note_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)

):
    return notes_service.delete_note(db, current_user, note_id)

@router.post("/notes/{note_id}/summarize", response_model=NoteSummaryResponse)
def summarize_note(
    note_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return notes_service.summarize_note(db, current_user, note_id)