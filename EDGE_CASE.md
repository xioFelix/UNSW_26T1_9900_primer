# Edge Case Documentation

## Edge Case: Optional Mark Field When Creating Students

### 1) The Edge Case Identified

When creating a new student via `POST /students`, the specification states that the `mark` field is optional. However, the database schema requires a mark value (INTEGER type). This creates an edge case:

**What should happen when a student is created without providing a mark?**

Possible scenarios:
- Student just enrolled, hasn't received any marks yet
- Mark will be added later through an update operation
- Frontend might not send the mark field at all

### 2) How I Addressed This

**Solution:** Default mark value to 0 when not provided.

**Implementation in `backend/app.py` (lines 45):**
```python
mark = student_data.get("mark", 0)  # Default mark to 0 if not provided
```

**Rationale:**
- **Database compatibility**: Ensures we always pass a valid integer to the database
- **Semantic meaning**: A mark of 0 indicates "no mark assigned yet" rather than causing an error
- **Flexibility**: Allows creation of student records before marks are available
- **Easy updates**: Mark can be updated later via `PUT /students/{id}`
- **Stats calculation**: The `/stats` endpoint correctly handles students with 0 marks

**Alternative approaches considered but rejected:**
- Using `NULL` in database: Would require schema changes
- Returning error 404: Too restrictive, prevents creating students without marks
- Using -1 as sentinel: Less intuitive than 0 for "no mark"