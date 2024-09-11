from sqlalchemy.orm import Session
import models, schemas, services

def create_user(db: Session, user: schemas.UserMatchingCreate) -> models.UserMatching:
    db_user = models.UserMatching(**user.model_dump())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user(db: Session, user_id: str) -> models.UserMatching:
    return db.query(models.UserMatching).filter(models.UserMatching.user_id == user_id).first()

def find_matches(db: Session, user: models.UserMatching, num_matches: int = 5) -> list[schemas.MatchResult]:
    return services.UserMatchingService.find_matches(db, user, num_matches)