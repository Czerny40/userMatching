import logging
from fastapi import FastAPI, Request, Form, Depends, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
import schemas
import crud
import database

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.post("/match", response_class=HTMLResponse)
async def match_users(
    request: Request,
    user_id: str = Form(...),
    height: float = Form(...),
    weight: float = Form(...),
    gender: str = Form(...),
    benchpress: float = Form(...),
    squat: float = Form(...),
    deadlift: float = Form(...),
    address: str = Form(...),
    db: Session = Depends(database.get_db),
):
    try:
        logger.debug(f"Received match request for user_id: {user_id}")
        user_data = schemas.UserMatchingCreate(
            user_id=user_id,
            height=height,
            weight=weight,
            gender=gender,
            benchpress=benchpress,
            squat=squat,
            deadlift=deadlift,
            address=address,
        )
        logger.debug(f"Created user_data: {user_data}")

        db_user = crud.create_user(db, user_data)
        logger.debug(f"Created db_user: {db_user}")

        matches = crud.find_matches(db, db_user)
        logger.debug(f"Found matches: {matches}")

        return templates.TemplateResponse(
            "matchingResults.html", {"request": request, "matches": matches}
        )
    except ValueError as e:
        logger.error(f"ValueError in match_users: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Unexpected error in match_users: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)