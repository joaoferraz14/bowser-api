UPDATE fastapi.public.posts
SET title = %s
   , content = %s
   , published = %s
WHERE id = %s
RETURNING *