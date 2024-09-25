import math
from typing import List
from sqlalchemy.orm import Session
import models, schemas

class UserMatchingService:
    @staticmethod
    def get_total_weight(user: models.UserMatching) -> float:
        return user.benchpress + user.squat + user.deadlift

    @staticmethod
    def get_ipf_gl_points(user: models.UserMatching) -> float:
        total = UserMatchingService.get_total_weight(user)
        if user.gender == "M":
            a, b, c = 1199.72839, 1025.18162, 0.00921
        else:
            a, b, c = 610.32796, 1045.59282, 0.03048
        ipf_gl_point = 100 * total / (a - b * math.exp(-c * user.weight))
        return max(0, ipf_gl_point)

    @staticmethod
    def calculate_similarity(user1: models.UserMatching, user2: models.UserMatching) -> float:
        height_diff = abs(user1.height - user2.height) / 50
        strength_diff = abs(UserMatchingService.get_ipf_gl_points(user1) - UserMatchingService.get_ipf_gl_points(user2)) / 500
        gender_penalty = user1.gender != user2.gender
        return height_diff * 0.1 + strength_diff * 0.5 + gender_penalty * 0.1

    @staticmethod
    def find_matches(db: Session, target_user: models.UserMatching, num_matches: int = 5) -> List[schemas.MatchResult]:
        users = db.query(models.UserMatching).filter(models.UserMatching.user_id != target_user.user_id).all()
        similarities = [
            schemas.MatchResult(
                user_id=user.user_id,
                similarity=UserMatchingService.calculate_similarity(target_user, user),
                ipf_score=UserMatchingService.get_ipf_gl_points(user)
            )
            for user in users
        ]
        similarities.sort(key=lambda x: x.similarity)
        return similarities[:num_matches]