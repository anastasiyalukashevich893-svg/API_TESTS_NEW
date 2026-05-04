import random
from services.university.models.grade_request import GradeRequest
from services.university.models.university_service import UniversityService


class TestGradeStatistics:
    def test_grades_students(self, university_api_utils_admin, create_teacher, create_group,
                             student_factory):
        university_service = UniversityService(university_api_utils_admin)
        students = [student_factory() for _ in range(3)]
        all_grades = []
        students_grades = {}

        for student in students:
            grades_count = random.randint(3, 5)
            student_grades = []

            for _ in range(grades_count):
                grade_value = random.randint(2, 5)
                student_grades.append(grade_value)
                all_grades.append(grade_value)

                university_service.create_grade(
                    GradeRequest(
                        teacher_id=create_teacher.id,
                        student_id=student.id,
                        grade=grade_value
                    )
                )

            students_grades[student.id] = student_grades

        teacher_stats = university_service.get_grade(teacher_id=create_teacher.id)

        expected_count = len(all_grades)
        expected_avg = round(sum(all_grades) / expected_count, 2)
        expected_min = min(all_grades)
        expected_max = max(all_grades)

        assert teacher_stats.count == expected_count, \
            f"Count mismatch: {teacher_stats.count} != {expected_count}"
        assert teacher_stats.min == expected_min, \
            f"Min mismatch: {teacher_stats.min} != {expected_min}"
        assert teacher_stats.max == expected_max, \
            f"Max mismatch: {teacher_stats.max} != {expected_max}"
        assert round(teacher_stats.avg, 2) == expected_avg, \
            f"Avg mismatch: {round(teacher_stats.avg, 2)} != {expected_avg}"
