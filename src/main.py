from fastapi import FastAPI, HTTPException
from schemas.models import Post

app = FastAPI()

my_posts = []


def find_post(id):
    post = next((post for post in my_posts if post["id"] == id), None)
    if post:
        return {"data": post}
    raise HTTPException(
        status_code=404, detail="Post not found - check if the id is correct"
    )


def get_max_id_from_posts():
    return max((post["id"] for post in my_posts), default=0)


@app.get("/status", status_code=200)
def root():
    return {"Message": f"Server is running"}


@app.get("/posts")
def get_posts():
    return {"data": my_posts}


@app.post("/posts")
async def create_post(post: Post):
    post_dict = post.dict()
    max_id = get_max_id_from_posts()
    post_dict["id"] = max_id + 1
    my_posts.append(post_dict)
    return {"data": post_dict}


@app.get("/posts/latest")
def get_latest_post():
    id = get_max_id_from_posts()
    data = find_post(int(id))
    return {"data": data}


@app.get("/posts/{id}")
def get_post_by_id(id: int):
    data = find_post(id)
    return {"data": data}
