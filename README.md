# bowser-api

**Version:** 0.1.0

bowser-api is a FastAPI project for managing posts. This documentation outlines the available endpoints and provides installation instructions.

## Installation

To run the application, follow these steps:

1. Install the required packages by running the following command:

    ```bash
    pip install -r requirements.txt
    ```

2. Start the application with uvicorn.

    ```bash
    uvicorn app-sqlalchemy.api.main:app
    ```

## API Endpoints

### `/status`

- **Method:** `GET`
- **Summary:** Check the server status.
- **Responses:** 
  - **200 OK:** The server is running.

### `/posts`

- **Method:** `GET`
- **Summary:** Retrieve all posts.
- **Query Parameters:**
  - `limit` (Optional, Integer): Limit the number of posts to retrieve (default is 10).
  - `skip` (Optional, Integer): Skip the first N posts (default is 0).
  - `search` (Optional, String): Search posts by title keyword.
- **Responses:** 
  - **200 OK:** Successfully retrieved posts.

- **Method:** `POST`
- **Summary:** Create a new post.
- **Request Body:** Post object with required fields `title` and `content`.
- **Responses:** 
  - **201 Created:** Post created successfully.
  - **422 Unprocessable Entity:** Validation error.

### `/posts/{id}`

- **Method:** `GET`
- **Summary:** Retrieve a post by ID.
- **Parameters:** `id` (Path parameter, Required, Integer)
- **Responses:** 
  - **200 OK:** Successfully retrieved the post.
  - **404 Not Found:** Post not found.
  - **422 Unprocessable Entity:** Validation error.

- **Method:** `PUT`
- **Summary:** Update a post by its ID.
- **Parameters:** `id` (Path parameter, Required, Integer)
- **Request Body:** Updated Post object.
- **Responses:** 
  - **202 Accepted:** Post updated successfully.
  - **404 Not Found:** Post not found.
  - **422 Unprocessable Entity:** Validation error.

- **Method:** `DELETE`
- **Summary:** Delete a post by its ID.
- **Parameters:** `id` (Path parameter, Required, Integer)
- **Responses:** 
  - **204 No Content:** Post deleted successfully.
  - **404 Not Found:** Post not found.

## Schema Definitions

- **Post:** Represents a post with required fields `title` and `content`.

STOPPED AT 9:27:55