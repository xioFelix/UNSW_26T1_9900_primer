# Edge Case Documentation

## 1. Optional Mark Field (POST /students)

The spec says `mark` is optional when creating a student, but the database expects an integer. If no mark is provided, I default it to `0` so the insert doesn't fail. This also keeps `/stats` calculations simple since every student has a numeric mark.

```python
mark = student_data.get("mark", 0)
```

## 2. Empty Database Stats (GET /stats)

When there are no students, calling `min()`, `max()` on an empty list raises an error, and dividing by zero for `average` crashes. I handle this by returning all values as `0` with status 200 when the student list is empty.

## 3. Missing or Empty Required Fields (POST /students)

The request body might be `null`, missing `name`/`course` keys, or have empty strings. I check for all three cases and return 404 with an error message if any of them occur.

## 4. Non-existent Student (PUT/DELETE /students/{id})

For PUT, I check if the student exists before updating and return 404 if not found. For DELETE, I check the return value from the database and return 404 if nothing was deleted.

## 5. Partial Updates (PUT /students/{id})

The spec doesn't say whether all fields are required on update. I allow partial updates where only the provided fields are changed and the rest keep their current values, so the client doesn't have to resend the entire object.
