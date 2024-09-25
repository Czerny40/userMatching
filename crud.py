from sqlalchemy.orm import Session
import models, schemas, services


def create_or_update_user(
    db: Session, user: schemas.UserMatchingCreate
) -> models.UserMatching:
    existing_user = get_user(db, user.user_id)
    if existing_user:
        # Update existing user
        for key, value in user.model_dump().items():
            setattr(existing_user, key, value)
    else:
        # Create new user
        existing_user = models.UserMatching(**user.model_dump())
        db.add(existing_user)

    db.commit()
    db.refresh(existing_user)
    return existing_user


def get_user(db: Session, user_id: str) -> models.UserMatching:
    return (
        db.query(models.UserMatching)
        .filter(models.UserMatching.user_id == user_id)
        .first()
    )


def find_matches(
    db: Session, user: models.UserMatching, num_matches: int = 5
) -> list[schemas.MatchResult]:
    return services.UserMatchingService.find_matches(db, user, num_matches)
