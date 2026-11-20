from langchain_core.tools import tool

COURSES: dict[int, list[tuple[str, str, float]]] = {
    1: [
        ("MS-251", "Probability & Statistics", 3.0),
        ("GE-160", "Applications of ICT", 3.0),
        ("GE-169", "Applied Physics", 3.0),
        ("GE-167", "Discrete Structures", 3.0),
        ("HQ-001", "Quran Translation I", 0.5),
        ("GE-190", "Functional English", 3.0),
    ],
    2: [
        ("CC-112", "Programming Fundamentals", 3.0),
        ("CC-112-L", "Programming Fundamentals Lab", 1.0),
        ("CC-110", "Digital Logic Design", 2.0),
        ("CC-110-L", "Digital Logic Design Lab", 1.0),
        ("MS-252", "Linear Algebra", 3.0),
        ("GE-191", "Expository Writing", 3.0),
        ("GE-163", "Islamic Studies", 2.0),
        ("HQ-002", "Quran Translation - II", 0.5),
    ],
    3: [
        ("CC-211", "Object Oriented Programming", 3.0),
        ("CC-211-L", "Object Oriented Programming Lab", 1.0),
        ("CC-215", "Database Systems", 3.0),
        ("CC-215-L", "Database Systems Lab", 1.0),
        ("CC-210", "Computer Organization & Assembly Language", 3.0),
        ("GE-162", "Calculus & Analytical Geometry", 3.0),
        ("GE-192", "Introduction to Management", 2.0),
        ("HQ-003", "Quran Translation - III", 0.5),
    ],
    4: [
        ("CC-213", "Data Structures", 3.0),
        ("CC-213-L", "Data Structures Lab", 1.0),
        ("CC-312", "Information Security", 3.0),
        ("CC-214", "Computer Networks", 3.0),
        ("CC-212", "Software Engineering", 3.0),
        ("DC-220", "Advanced Database Management Systems", 3.0),
        ("HQ-004", "Quran Translation - IV", 0.5),
    ],
    5: [
        ("CC-313", "Analysis of Algorithms", 3.0),
        ("CC-310", "Artificial Intelligence", 3.0),
        ("DC-320", "Theory of Automata and Formal Languages", 3.0),
        ("DC-321", "Human Computer Interaction", 3.0),
        ("DC-322", "Computer Architecture", 3.0),
        ("EC-330", "Web Technologies / Elective", 3.0),
        ("HQ-005", "Quran Translation - V", 0.5),
    ],
    6: [
        ("CC-311", "Operating Systems", 3.0),
        ("EC-333", "Mobile Application Development / Elective", 3.0),
        ("EC-324", "Software Construction & Development / Elective", 3.0),
        ("EC-335", "Machine Learning / Elective", 3.0),
        ("EC-334", "Game Design and Development / Elective", 3.0),
        ("MS-253", "Multivariable Calculus", 3.0),
        ("HQ-006", "Quran Translation - VI", 0.5),
    ],
    7: [
        ("CC-411", "Final Year Project I", 2.0),
        ("DC-328", "Parallel & Distributed Computing", 3.0),
        ("EC-345", "Computer Vision / Elective", 3.0),
        ("EC-425", "Software Quality Engineering / Elective", 3.0),
        ("MS-254", "Technical and Business Writing", 3.0),
        ("GE-263", "Entrepreneurship", 2.0),
        ("GE-262", "Professional Practices", 2.0),
        ("HQ-007", "Quran Translation - VII", 0.5),
    ],
    8: [
        ("CC-412", "Final Year Project II", 4.0),
        ("DC-421", "Compiler Construction", 3.0),
        ("UE-272", "Introduction to Marketing", 3.0),
        ("GE-168", "Ideology and Constitution of Pakistan", 2.0),
        ("GE-363", "Civics and Community Engagement", 2.0),
        ("HQ-008", "Quran Translation - VIII", 0.5),
    ],
}


def marks_to_grade_points(marks: int) -> float:
    """Convert numerical course marks (0 to 100) to official PUCIT grade points according to section 5.1.
    Use this whenever a student specifies raw marks for a subject.
    """
    if marks < 0 or marks > 100:
        return "Error: marks must be between 0 and 100"
    if marks >= 85:
        return 4.0
    elif marks >= 80:
        return 3.7
    elif marks >= 75:
        return 3.3
    elif marks >= 70:
        return 3.0
    elif marks >= 65:
        return 2.7
    elif marks >= 61:
        return 2.3
    elif marks >= 58:
        return 2.0
    elif marks >= 55:
        return 1.7
    elif marks >= 50:
        return 1.0
    else:
        return 0.0


def calculate_semester_gpa(
    grade_points: list[float], credit_hours: list[float]
) -> float:
    """Calculate the credit-weighted GPA for a semester using lists of grade points and credit hours.
    Use this when you have the grade points and credit hours for all courses in a semester.
    """
    if not grade_points or not credit_hours:
        return "Error: grade_points and credit_hours cannot be empty"
    if len(grade_points) != len(credit_hours):
        return "Error: grade_points and credit_hours must have the same length"
    total_ch = sum(credit_hours)
    if any(gp < 0.0 or gp > 4.0 for gp in grade_points):
        return "Error: every grade point must be between 0.0 and 4.0"
    if any(ch <= 0 for ch in credit_hours):
        return "Error: every credit hour value must be greater than 0"
    total_ch = sum(credit_hours)
    if total_ch <= 0:
        return "Error: total credit hours must be greater than 0"
    weighted_sum = sum(gp * ch for gp, ch in zip(grade_points, credit_hours))
    return round(weighted_sum / total_ch, 2)


def calculate_new_cgpa(
    current_cgpa: float,
    completed_credit_hours: float,
    semester_gpa: float,
    semester_credit_hours: float,
) -> float:
    """Project the new cumulative GPA (CGPA) after one semester.
    Use this when the student provides their current CGPA, completed credit hours,
    and wants to determine the impact of an upcoming semester's GPA.
    """
    if current_cgpa < 0.0 or current_cgpa > 4.0:
        return "Error: current_cgpa must be between 0.0 and 4.0"
    if semester_gpa < 0.0 or semester_gpa > 4.0:
        return "Error: semester_gpa must be between 0.0 and 4.0"
    if completed_credit_hours < 0 or semester_credit_hours <= 0:
        return "Error: completed_credit_hours must be non-negative and semester_credit_hours must be positive"

    total_ch = completed_credit_hours + semester_credit_hours
    new_cgpa = ((current_cgpa * completed_credit_hours)+ (semester_gpa * semester_credit_hours)) / total_ch
    return round(new_cgpa, 2)


def required_gpa_for_target(
    target_cgpa: float,
    current_cgpa: float,
    completed_credit_hours: float,
    remaining_credit_hours: float,
) -> float:
    """Calculate the average GPA needed over remaining credit hours to reach a target CGPA.
    Args:
        target_cgpa: Desired final CGPA on a 4.0 scale (argument name must be target_cgpa).
        current_cgpa: Current CGPA on a 4.0 scale.
        completed_credit_hours: Credit hours already earned.
        remaining_credit_hours: Credit hours still to be taken (must be > 0).
    """
    if target_cgpa < 0.0 or target_cgpa > 4.0:
        return "Error: target_cgpa must be between 0.0 and 4.0"
    if current_cgpa < 0.0 or current_cgpa > 4.0:
        return "Error: current_cgpa must be between 0.0 and 4.0"
    if remaining_credit_hours <= 0:
        return "Error: remaining_credit_hours must be greater than 0"
    if completed_credit_hours < 0:
        return "Error: completed_credit_hours must be non-negative"

    total_ch = completed_credit_hours + remaining_credit_hours
    req_gpa = ((target_cgpa * total_ch) - (current_cgpa * completed_credit_hours)) / remaining_credit_hours
    if req_gpa <= 0:
        return 0.0 
    return round(req_gpa, 2)


def get_semester_courses(semester: int) -> str:
    """Return the official list of courses, course codes, and credit hours for a PUCIT BS(CS) semester (1 to 8).
    Use this when checking course names, codes, or semester credit hour totals.
    """
    if semester not in COURSES:
        return "Error: semester must be between 1 and 8"

    courses = COURSES[semester]
    sem_total = sum(ch for _, _, ch in courses)
    course_list = [
        f"- {code}: {name} ({ch} CH)" for code, name, ch in courses
    ]
    return f"Semester {semester} Courses (Total {sem_total} CH):\n" + "\n".join(course_list)


def get_remaining_credit_hours(current_semester: int) -> float:
    """Total the graded credit hours remaining after a completed semester (e.g., passing semester 4 gives hours for 5 to 8).
    Use this when computing total hours left for graduation projections.
    """
    if current_semester < 0 or current_semester > 8:
        return "Error: semester must be between 1 and 8"
    if current_semester == 8:
        return 0.0

    remaining = sum(
        sum(ch for _, _, ch in courses)
        for sem, courses in COURSES.items()
        if sem > current_semester
    )
    return round(remaining, 2)


def save_report(filename: str, content: str) -> str:
    """Save an academic summary or GPA projection report to a local text file and return a confirmation.
    Use this ONLY when the student explicitly requests to save their results or summary.
    """
    try:
        with open(filename, "w", encoding="utf-8") as f:
            f.write(content)
        return f"Report successfully saved to {filename}."
    except Exception as e:
        return f"Error saving report: {str(e)}"