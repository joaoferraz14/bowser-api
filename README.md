# bowser-api

**Version:** 0.1.0

This is a FastAPI project to manage posts. This documentation describes the endpoints available in this API.

## Installation

First, you'll need to install the required packages. You can do this by running the following command:

```bash
pip install -r requirements.txt
uvicorn app.api.main:app --reload
```
The --reload flag enables hot reloading, which means the server will automatically update whenever you make changes to the code.

## API Endpoints

### `/status`

- **Method:** `GET`
- **Summary:** Server status endpoint. Returns a status message.
- **Responses:** 
  - **200:** Successful Response

### `/posts`

- **Method:** `GET`
- **Summary:** Endpoint to get all the posts.
- **Responses:** 
  - **200:** Successful Response

- **Method:** `POST`
- **Summary:** Endpoint to create a new post.
- **Responses:** 
  - **201:** Successful Response
  - **422:** Validation Error

### `/posts/{id}`

- **Method:** `GET`
- **Summary:** Endpoint to get a post by id.
- **Parameters:** `id` (Path parameter, Required, Integer)
- **Responses:** 
  - **200:** Successful Response
  - **422:** Validation Error

- **Method:** `PUT`
- **Summary:** Update a post by its ID.
- **Parameters:** `id` (Path parameter, Required, Integer)
- **Responses:** 
  - **202:** Successful Response
  - **422:** Validation Error

- **Method:** `DELETE`
- **Summary:** Delete a post by its ID.
- **Parameters:** `id` (Path parameter, Required, Integer)
- **Responses:** 
  - **204:** Successful Response
  - **422:** Validation Error

## Schema Definitions

- **Post:** Object that represents a post, required fields are `title` and `content`. 
