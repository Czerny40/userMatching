import logging
from fastapi import FastAPI, Request, Form, Depends, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware
from database import engine
from pydantic import BaseModel

import models
import schemas
import crud
import database

# 로깅 설정
logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080"],  # Spring Boot server address
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

templates = Jinja2Templates(directory="templates")

models.Base.metadata.create_all(bind=engine)


class UserData(BaseModel):
    user_id: str


@app.post("/matching-form", response_class=HTMLResponse)
async def matching_form(request: Request, user_data: UserData):
    logger.debug(f"Rendering matching form for user: {user_data.user_id}")
    return templates.TemplateResponse(
        "matchingForm.html", {"request": request, "user_id": user_data.user_id}
    )


@app.get("/matching-form", response_class=HTMLResponse)
async def matching_form(request: Request):
    logger.debug("Rendering matching form")
    return templates.TemplateResponse("matchingForm.html", {"request": request})


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
    logger.debug(f"Received match request for user_id: {user_id}")
    try:
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

        try:
            response = templates.TemplateResponse(
                "matchingResults.html", {"request": request, "matches": matches}
            )
            logger.debug("Template rendered successfully")
            return response
        except Exception as template_error:
            logger.error(
                f"Template rendering error: {str(template_error)}", exc_info=True
            )
            raise HTTPException(
                status_code=500,
                detail=f"Template rendering error: {str(template_error)}",
            )

    except ValueError as e:
        logger.error(f"ValueError in match_users: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Unexpected error in match_users: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500, detail=f"An unexpected error occurred: {str(e)}"
        )


if __name__ == "__main__":
    import uvicorn

    logger.info("Starting the application")
    uvicorn.run(app, host="0.0.0.0", port=8000)
