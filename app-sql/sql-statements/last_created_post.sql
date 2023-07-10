SELECT *
FROM fastapi.public.posts
WHERE id IN (
    SELECT max(id) FROM fastapi.public.posts
    );
