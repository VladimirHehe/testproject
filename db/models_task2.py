from sqlalchemy import Column, Integer, String, ForeignKey, Date, Boolean, CheckConstraint
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime, timedelta
from sqlalchemy.orm import relationship

Base = declarative_base()


class Player(Base):
    __tablename__ = 'players'
    id = Column(Integer, primary_key=True)
    player_id = Column(Integer, unique=True)
    prizes = relationship("Prize", secondary="player_prizes", backref="players")


class Level(Base):
    __tablename__ = 'levels'
    id = Column(Integer, primary_key=True)
    title = Column(String(100))
    order = Column(Integer, default=0)


class Prize(Base):
    __tablename__ = 'prizes'
    id = Column(Integer, primary_key=True)
    title = Column(String)


class Player_Level(Base):
    __tablename__ = 'player_levels'
    id = Column(Integer, primary_key=True)
    player_id = Column(Integer, ForeignKey('players.player_id'))
    level_id = Column(Integer, ForeignKey('levels.id'))
    completed = Column(Date)
    is_completed = Column(Boolean, default=False)
    score = Column(Integer, default=0)
    player = relationship("Player", cascade="all, delete", backref="player_levels", )
    level = relationship("Level", cascade="all, delete", backref="player_levels", )
    __table_args__ = (
        CheckConstraint(score >= 0, name='check_score_positive'),
        {})


class Level_Prize(Base):
    __tablename__ = 'level_prizes'
    id = Column(Integer, primary_key=True)
    level_id = Column(Integer, ForeignKey('levels.id'))
    prize_id = Column(Integer, ForeignKey('prizes.id'))
    received = Column(Date)
    level = relationship("Level", cascade="all, delete", backref="level_prizes", )
    prize = relationship("Prize", cascade="all, delete", backref="level_prizes", )


class Player_Prize(Base):
    __tablename__ = 'player_prizes'
    id = Column(Integer, primary_key=True)
    player_id = Column(Integer, ForeignKey('players.player_id'))
    prize_id = Column(Integer, ForeignKey('prizes.id'))
    player = relationship(Player, cascade="all, delete", backref='players_prizes')
    prize = relationship(Prize, cascade="all, delete", backref='players_prizes')
