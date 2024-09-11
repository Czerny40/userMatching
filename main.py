from fastapi import FastAPI, Request, Form, Depends, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware
from database import engine

import models
import schemas
import crud
import database

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


@app.get("/matching-form", response_class=HTMLResponse)
async def matching_form(request: Request):
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
        db_user = crud.create_user(db, user_data)
        matches = crud.find_matches(db, db_user)
        return templates.TemplateResponse(
            "matchingResults.html", {"request": request, "matches": matches}
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="An unexpected error occurred")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
