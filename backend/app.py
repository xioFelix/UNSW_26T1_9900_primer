from flask import Flask, jsonify, request
from flask_cors import CORS

import db

app = Flask(__name__)
CORS(app)

# Instructions:
# - Use the functions in backend/db.py in your implementation.
# - You are free to use additional data structures in your solution
# - You must define and tell your tutor one edge case you have devised and how you have addressed this

@app.route("/students")
def get_students():
    """
    Route to fetch all students from the database
    return: Array of student objects
    """
    try:
        students = db.get_all_students()
        return jsonify(students), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 404


@app.route("/students", methods=["POST"])
def create_student():
    """
    Route to create a new student
    param name: The name of the student (from request body)
    param course: The course the student is enrolled in (from request body)
    param mark: The mark the student received (from request body)
    return: The created student if successful
    """
    try:
        student_data = request.json

        # Validate required fields
        if not student_data or "name" not in student_data or "course" not in student_data:
            return jsonify({"error": "Name and course are required"}), 404

        name = student_data.get("name")
        course = student_data.get("course")
        mark = student_data.get("mark", 0)  # Default mark to 0 if not provided

        # Validate name and course are not empty
        if not name or not course:
            return jsonify({"error": "Name and course cannot be empty"}), 404

        # Create student in database
        created_student = db.insert_student(name, course, mark)
        return jsonify(created_student), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 404


@app.route("/students/<int:student_id>", methods=["PUT"])
def update_student(student_id):
    """
    Route to update student details by id
    param name: The name of the student (from request body)
    param course: The course the student is enrolled in (from request body)
    param mark: The mark the student received (from request body)
    return: The updated student if successful
    """
    try:
        student_data = request.json

        # Check if student exists
        existing_student = db.get_student_by_id(student_id)
        if not existing_student:
            return jsonify({"error": "Student not found"}), 404

        # Extract fields from request (all optional for update)
        name = student_data.get("name") if student_data else None
        course = student_data.get("course") if student_data else None
        mark = student_data.get("mark") if student_data else None

        # Update student in database
        updated_student = db.update_student(student_id, name, course, mark)
        return jsonify(updated_student), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 404


@app.route("/students/<int:student_id>", methods=["DELETE"])
def delete_student(student_id):
    """
    Route to delete student by id
    return: The deleted student
    """
    try:
        # Attempt to delete student
        result = db.delete_student(student_id)

        if not result:
            return jsonify({"error": "Student not found"}), 404

        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 404


@app.route("/stats")
def get_stats():
    """
    Route to show the stats of all student marks
    return: An object with the stats (count, average, min, max)
    """
    try:
        students = db.get_all_students()

        # Handle case when there are no students
        if not students:
            return jsonify({
                "count": 0,
                "average": 0,
                "min": 0,
                "max": 0
            }), 200

        # Extract marks from students
        marks = [student["mark"] for student in students if student.get("mark") is not None]

        # Handle case when no students have marks
        if not marks:
            return jsonify({
                "count": len(students),
                "average": 0,
                "min": 0,
                "max": 0
            }), 200

        # Calculate statistics
        stats = {
            "count": len(marks),
            "average": round(sum(marks) / len(marks), 2),
            "min": min(marks),
            "max": max(marks)
        }

        return jsonify(stats), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 404


@app.route("/")
def health():
    """Health check."""
    return {"status": "ok"}


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
