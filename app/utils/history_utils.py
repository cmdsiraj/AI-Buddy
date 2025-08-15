from sqlalchemy.orm import Session
from .. import models


def _history(db: Session, username: str) -> list[dict]:
    conv = db.query(models.Conversation).filter_by(username=username).first()
    if not conv:
        return []
    return [{"role": m.role, "content": m.content} for m in conv.messages]

def _save_chat(db: Session, username: str, history: list[dict]):
    # Overwrite old messages
    conv = db.query(models.Conversation).filter_by(username=username).first()
    if not conv:
        conv = models.Conversation(username=username)
        db.add(conv)
        db.commit()
        db.refresh(conv)

    # Clear existing messages
    db.query(models.ChatMessage).filter_by(conversation_id=conv.id).delete()

    # Insert new messages
    for msg in history:
        db.add(models.ChatMessage(
            conversation_id=conv.id,
            role=msg["role"],
            content=msg["content"]
        ))
    db.commit()

def _clear_history(db: Session, username: str):
    print("deleting")
    conv = db.query(models.Conversation).filter_by(username=username).first()
    if conv:
        db.query(models.ChatMessage).filter_by(conversation_id=conv.id).delete()
        db.commit()
    after = db.query(models.ChatMessage).filter_by(conversation_id=conv.id).count()
    print("after delete:", after)
