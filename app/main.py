from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from datetime import date
from random import randrange

app = FastAPI()

# Schemas


class Comment(BaseModel):
    content: str
    date_posted: date
    user_id: int


class Team(BaseModel):
    title: str
    tags: list[str]
    published: bool = False
    date_posted: date
    likes: Optional[int] = None
    user_id: int
    comments: Optional[list[Comment]] = None
    # pals: list[Pal]


# Testing Data
my_comments = [{"content": "This comment is helpful",
                "date_posted": "2024-03-27", "user_id": 1, "id": 1}]
my_teams = [{"title": "Awesome Team", "tags": ["PVP", "Exploration"], "published": False,
             "date_posted": "2024-03-27", "likes": None, "user_id": 1, "comments": my_comments, "id": 1}]


# Helper Functions
def find_comment(id: int):
    if my_comments:
        for comment in my_comments:
            if comment.get("id") == id:
                return comment
        return
    return

# Routes


@app.get("/")
def read_root():
    return {"message": "Welcome to Pal Pal"}

    # Teams


@app.get("/teams")
def get_teams():
    return {"data": my_teams}


@app.get("/teams/{id}")
def get_team(id):
    return {"team": id}


@app.post("/teams")
def create_team(team: Team):
    team_dict = team.dict()
    team_dict["id"] = randrange(0, 1000000)
    my_teams.append(team_dict)
    return {"data": team_dict}

    # Comments


@app.get("/comments")
def get_comments():
    return {"data": my_comments}


@app.get("/comments/{id}")
def get_comment(id):
    comment = find_comment(int(id))
    return {"data": comment}


@app.post("/comments")
def create_comment(comment: Comment):
    comment_dict = comment.dict()
    comment_dict["id"] = randrange(0, 1000000)
    my_comments.append(comment_dict)
    return {"data": comment_dict}
