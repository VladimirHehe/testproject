import os

from fastapi import HTTPException
from db.DataBase import Session_factory, engine
from db.models_task2 import *
import pandas as pd


class Core:
    @staticmethod
    def award_prize(player_id: int, level_id: int, ):
        with Session_factory() as db:
            player = db.query(Player).get(player_id)
            level = db.query(Level).get(level_id)

            if player and level:
                player_level = db.query(Player_Level).filter_by(player_id=player_id, level_id=level_id).first()
                if player_level and player_level.is_completed:
                    level_prize = db.query(Level_Prize).filter_by(level_id=level_id).first()
                    if level_prize:
                        prize = level_prize.prize
                        player.prizes.append(prize)
                        db.commit()
                        return {
                            "message": f"Prize {prize.title} awarded to player {player_id} for completing level {level_id}"}
                    else:
                        raise HTTPException(status_code=404, detail="No prize associated with this level")
                else:
                    raise HTTPException(status_code=400, detail="Player has not completed this level")
            else:
                raise HTTPException(status_code=404, detail="Player or level not found")

    @staticmethod
    def dump_csv():
        select_data = """
        SELECT 
          p.player_id AS player_id,
          l.title AS level_title,
          pl.is_completed AS is_level_completed,
          pr.title AS prize_title
        FROM 
          players p
          LEFT JOIN player_levels pl ON p.player_id = pl.player_id
          LEFT JOIN levels l ON pl.level_id = l.id
          LEFT JOIN level_prizes lp ON l.id = lp.level_id
          LEFT JOIN prizes pr ON lp.prize_id = pr.id
          LEFT JOIN player_prizes pp ON p.player_id = pp.player_id AND pr.id = pp.prize_id
        LIMIT 100;
        """
        basedir = os.path.abspath(os.path.dirname(__file__))
        result = pd.read_sql_query(select_data, engine)
        result.to_csv(os.path.join(basedir, 'DumpDB.csv'), index=False, sep=";")
