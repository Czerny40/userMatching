from sqlalchemy import Column, Integer, Float, String, CheckConstraint
from sqlalchemy.orm import validates
from database import Base

class UserMatching(Base):
    __tablename__ = "userMatching"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String(100), nullable=False)
    height = Column(Float, CheckConstraint('height > 0'))
    weight = Column(Float, CheckConstraint('weight > 0'))
    gender = Column(String(1))
    benchpress = Column(Float, CheckConstraint('benchpress >= 0'))
    squat = Column(Float, CheckConstraint('squat >= 0'))
    deadlift = Column(Float, CheckConstraint('deadlift >= 0'))
    address = Column(String(255))
    latitude = Column(Float)
    longitude = Column(Float)

    @validates('gender')
    def validate_gender(self, key, gender):
        assert gender in ['M', 'F'], "Gender must be either 'M' or 'F'"
        return gender

    __table_args__ = (
        CheckConstraint('gender IN ("M", "F")'),
    )