from fastapi import FastAPI, Request, HTTPException, status
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as starletteHTTPException
from schemas import PostCreate, PostResponse

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")


posts: list[dict] = [
    {
        "id": 1,
        "author": "Raieyan Aziz",
        "title": "Chole bhature ya puri sabzi",
        "content": "Chole bhature is better beacuse its tastier",
        "date_posted": "september 30, 2026",
    },
    {
        "id": 2,
        "author": "Piyush Mishra",
        "title": "apple is better!",
        "content": "apple never copies",
        "date_posted": "sept 20, 2026",
    },
]

@app.get("/", include_in_schema= False, name="home")
@app.get("/posts", include_in_schema=False, name="post")
def home(request: Request):
    return templates.TemplateResponse(request, "home.html", {"posts": posts, "title": "HOME"})

@app.get("/posts/{post_id}")
def post_page(request: Request, post_id: int):
    for post in posts:
        if post.get("id") == post_id:
            title = post["title"][:50]
            return templates.TemplateResponse(request, "post.html", {"post": post, "title": title})
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)


@app.get("/api/posts", response_model=list[PostResponse]) #response model verifies from return post and check for matching type hints
def get_posts():
    return posts


#create post
@app.post("/api/posts", response_model=PostResponse, status_code= status.HTTP_201_CREATED)
def create_post(post: PostCreate):
    new_id = max(p["id"] for p in posts) + 1 if posts else 1
    new_post = {
        "id": new_id,
        "title": post.title,
        "author": post.author,
        "content": post.content,
        "date_posted": "03 oct 2026"        
    }
    posts.append(new_post)
    return new_post


@app.get("/api/posts/{post_id}", response_model=PostResponse)
def get_post(post_id: int):
    for post in posts:
        if post.get("id") == post_id:
            return post
    raise HTTPException(status_code=status.HTTP_402_PAYMENT_REQUIRED)




