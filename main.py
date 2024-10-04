from fastapi import FastAPI
import uvicorn
from core.coretask2 import Core

app = FastAPI()


@app.post("/award_prize")
def award_prize(player_id: int, level_id: int):
    try:
        result = Core.award_prize(player_id, level_id)
        return result
    except Exception as e:
        return {"error": str(e)}


@app.get("/dump_data")
def dump_data():
    try:
        Core.dump_csv()
        return {"Dump": "success"}
    except Exception as e:
        return {"error": str(e)}


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
