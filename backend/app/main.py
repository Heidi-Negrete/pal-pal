from fastapi import FastAPI, Response, status, HTTPException, Query
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional, Annotated
from datetime import date
from random import randrange
from sqlmodel import Session
from .database import create_db_and_tables, engine
from .models import Team as TDB  # temporary alias to resolve namespace conflict


app = FastAPI()


@app.on_event("startup")
def on_startup():
    create_db_and_tables()

# Schemas


class Comment(BaseModel):
    content: str


class Pal(BaseModel):
    name: str
    skills: list[str] | None = None
    type: list[str] | None = None
    # soul allocation


class Team(BaseModel):
    title: str
    tags: list[str]
    published: bool = False
    pals: list[Pal]
    notes: str | None = None


# Testing Data
my_comments = [{"content": "This comment is helpful",
                "date_posted": "2024-03-27", "user_id": 1, "id": 1}]
my_teams = [{"title": "Awesome Team", "tags": ["PVP", "Exploration"], "published": False,
             "date_posted": "2024-03-27", "likes": None, "user_id": 1, "comments": my_comments, "team_id": 1}]


# Helper Functions
def find_comment(id: int):
    if my_comments:
        for index, comment in enumerate(my_comments):
            if comment.get("id") == id:
                return (comment, index)
        return (None, None)
    return (None, None)

# Routes


@app.get("/")
def read_root():
    return {"message": "Welcome to Pal Pal"}

    # Teams


@app.get("/teams")
def get_teams():
    return {"data": my_teams}


@app.get("/teams/latest")
def get_latest_teams():
    team = my_teams[-1]
    return team


@app.get("/teams/{id}")
def get_team(id: int):
    return {"team": id}


@app.post("/teams", status_code=status.HTTP_201_CREATED)
def create_team(team: Team):
    team_dict = team.dict()
    team_dict["team_id"] = randrange(0, 1000000)
    my_teams.append(team_dict)
    return {"data": team_dict}

    # Comments


@app.get("/comments")
def get_comments():
    return {"data": my_comments}


@app.get("/comments/{id}")
def get_comment(id: int):
    comment = find_comment(id)[0]
    if not comment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"comment with id: {id} was not found")
    return {"data": comment}


@app.post("/comments", status_code=status.HTTP_201_CREATED)
def create_comment(comment: Comment):
    comment_dict = comment.dict()
    comment_dict["id"] = randrange(0, 1000000)
    my_comments.append(comment_dict)
    return {"data": comment_dict}


@app.delete("/comments/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_comment(id: int):
    comment, index = find_comment(id)
    if index is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"comment with id {id} was not found")
    my_comments.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/comments/{id}")
def update_comment(id: int, comment: Comment):
    original_comment, index = find_comment(id)
    if index is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"comment with id {id} was not found")
    comment_dict = comment.dict()
    my_comments[index] = comment_dict
    my_comments[index]["id"] = id
    print(my_comments[index])
    return {"data": comment_dict}
