import logging
import requests
import math
import os
from dotenv import load_dotenv
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

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
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
    return templates.TemplateResponse(
        "matchingForm.html", {"request": request, "user_id": user_data.user_id}
    )


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
    page: int = Form(1),
    db: Session = Depends(database.get_db),
):
    try:
        KAKAO_API_KEY = os.getenv("KAKAO_API_KEY")
        kakao_url = "https://dapi.kakao.com/v2/local/search/address.json"
        headers = {"Authorization": f"KakaoAK {KAKAO_API_KEY}"}
        params = {"query": address}
        response = requests.get(kakao_url, headers=headers, params=params)
        response.raise_for_status()
        result = response.json()

        if not result["documents"]:
            raise ValueError("Invalid address")

        latitude = float(result["documents"][0]["y"])
        longitude = float(result["documents"][0]["x"])

        user_data = schemas.UserMatchingCreate(
            user_id=user_id,
            height=height,
            weight=weight,
            gender=gender,
            benchpress=benchpress,
            squat=squat,
            deadlift=deadlift,
            address=address,
            latitude=latitude,
            longitude=longitude,
        )

        db_user = crud.create_or_update_user(db, user_data)

        matches, total_matches = crud.find_matches(db, db_user, page)
        total_pages = math.ceil(total_matches / 5)

        try:
            response = templates.TemplateResponse(
                "matchingResults.html",
                {
                    "request": request,
                    "matches": matches,
                    "current_page": page,
                    "total_pages": total_pages,
                    "total_matches": total_matches,
                    "user_id": user_id,
                },
            )
            return response
        except Exception as template_error:
            raise HTTPException(
                status_code=500,
                detail=f"Template rendering error: {str(template_error)}",
            )

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except requests.RequestException as e:
        raise HTTPException(
            status_code=500, detail="Error communicating with Kakao API"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"An unexpected error occurred: {str(e)}"
        )


@app.get("/match/{user_id}/{page}", response_class=HTMLResponse)
async def get_matches(
    request: Request, user_id: str, page: int, db: Session = Depends(database.get_db)
):
    try:
        user = crud.get_user(db, user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        matches, total_matches = crud.find_matches(db, user, page)
        total_pages = math.ceil(total_matches / 5)

        return templates.TemplateResponse(
            "matchingResults.html",
            {
                "request": request,
                "matches": matches,
                "current_page": page,
                "total_pages": total_pages,
                "total_matches": total_matches,
                "user_id": user_id,
            },
        )
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"An unexpected error occurred: {str(e)}"
        )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
