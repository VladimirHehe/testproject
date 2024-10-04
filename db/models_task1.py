from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime, timedelta
from sqlalchemy.orm import relationship

Base = declarative_base()


class BoostType(Enum):
    XP_BOOST = 'xp_boost'
    SCORE_BOOST = 'score_boost'
    SPEED_BOOST = 'speed_boost'


class Player_model(Base):
    __tablename__ = 'player'
    id = Column(Integer, PrimaryKey=True)
    name = Column(String, unique=True, nullable=False)
    created_at = Column(DateTime, default=datetime.now)
    points = Column(Integer, default=0)
    last_login_at = Column(DateTime, default=datetime.now)

    def login(self):
        now = datetime.now()
        last_login_at = self.last_login_at + timedelta(days=1)

        if self.last_login_at < last_login_at:
            self.points += 100
            self.last_login_at = now


class Boost_model(Base):
    __tablename__ = 'boost'
    id = Column(Integer, primary_key=True)
    player_id = Column(Integer, ForeignKey('player.id'))
    player = relationship("Player_model", backref="boost")
    boost_type = Column(Enum(BoostType)) # ТИПЫ БУСТОВ

