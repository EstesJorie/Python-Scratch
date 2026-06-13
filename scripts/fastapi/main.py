import os

from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()  # create instance of FastAPI

templates = Jinja2Templates(directory="templates")  # set up templates
if templates is None:
    raise ValueError(
        "Templates directory not found. Please ensure the 'templates' folder exists."
    )

static_dir = "static"
if not os.path.isdir(static_dir):
    raise ValueError(
        f"Static directory '{static_dir}' not found. Please ensure the 'static' folder exists."
    )

app.mount("/static", StaticFiles(directory=static_dir), name="static")

posts: list[dict] = [
    {
        "id": 1,
        "author": "Joe Bloggs",
        "title": "FastAPI rules!",
        "content": "This was really easy to use and super fast.",
        "date_posted": "June 15, 2026",
    },
    {
        "id": 2,
        "author": "Joe Floggs",
        "title": "Python is great for this",
        "content": "Python is a good choice for web development backends.",
        "date_posted": "June 14, 2026",
    },
]


@app.get(
    "/", include_in_schema=False, name="home"
)  # define a route for the root endpoint
@app.get(
    "/posts", include_in_schema=False, name="posts"
)  # stack routes to the same function
def home(request: Request):  # define the function to handle the request
    return templates.TemplateResponse(
        request, "home.html", {"posts": posts, "title": "Home"}
    )  # render the template with the posts data


@app.get("/api/posts")
def get_posts():
    return posts
