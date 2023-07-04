from fastapi import FastAPI
from schemas.models import Post
app = FastAPI()


my_posts = [{"title": "title of post", "content": "content of post 1", "id": 1}, 
            {"title": "title of 2", "content": "content of post 2222", "id": 2}]


@app.get("/")
def root():
    return {"message": "joaozinho noia"}

@app.get("/posts")
def get_posts():
    return {"data": my_posts}


@app.post("/posts")
def create_post(post: Post):
    print(post.dict())
    return {"data": post}


# expected schema, title str, content str
