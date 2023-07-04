from fastapi import FastAPI
from fastapi.params import Body

app = FastAPI()


@app.get("/")
def root():
    return {"message": "joaozinho noia"}


@app.get("/posts")
def get_posts():
    return {"data": ["this is your post", "ola"]}


@app.post("/createposts")
def create_post(payload: dict = Body(...)):
    print(payload)
    return {"new post": f"title {payload['title']} content {payload['content']}"}


# expected schema, title str, content str
