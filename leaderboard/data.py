
from typing import List, Union



from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


from models_db.users import user
from models_db.leaderboard import leaderboard


class Data:
    def __init__(self) -> None:
        pass

    def get_user(self, username: str) -> Union[user, None]:
        return user.query.filter_by(username=username).first()
    def get_leaderboard(self, page : int) -> List[leaderboard]:
        return leaderboard.query.order_by(leaderboard.score.desc()).limit(10).offset(page*10).all()

    def get_leaderboard_count(self) -> int:
        return leaderboard.query.count()

    def get_user_best_score(self, user_id: int) -> Union[leaderboard, None]:
        return leaderboard.query.filter_by(user_id=user_id).order_by(leaderboard.score.desc()).first().score

    def get_list_user_scores(self, user_id: int) -> List[leaderboard]:
        return leaderboard.query.filter_by(user_id=user_id).order_by(leaderboard.score.desc()).all()
    def upload_score(self, user_id: int, score: int) -> None:
        new_score = leaderboard(user_id=user_id, score=score)
        db.session.add(new_score)
        db.session.commit()
