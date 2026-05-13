import random

from services.university.models.base_grade import GradesCount, MinMaxGrade
from services.university.models.grade_request import GradeRequest
from services.university.models.university_service import UniversityService
from utils.soft_assert import SoftAssert


class TestGradeStatistics:
    def test_grades_students(self, university_api_utils_admin, create_teacher, student_factory):
        university_service = UniversityService(university_api_utils_admin)
        students = [student_factory() for _ in range(3)]
        all_grades = []
        students_grades = {}

        for student in students:
            grades_count = random.randint(GradesCount.MIN_COUNT_GRADE, GradesCount.MAX_COUNT_GRADE)
            student_grades = []

            for _ in range(grades_count):
                grade_value = random.randint(MinMaxGrade.MIN_GRADE, MinMaxGrade.MAX_GRADE)
                student_grades.append(grade_value)
                all_grades.append(grade_value)

                university_service.create_grade(
                    GradeRequest(
                        teacher_id=create_teacher.id, student_id=student.id, grade=grade_value
                    )
                )

            students_grades[student.id] = student_grades

        teacher_stats = university_service.get_grade(teacher_id=create_teacher.id)

        expected_count = len(all_grades)
        expected_avg = round(sum(all_grades) / expected_count, 2)
        expected_min = min(all_grades)
        expected_max = max(all_grades)

        soft = SoftAssert()

        soft.assert_equal(teacher_stats.count, expected_count, "Count mismatch")
        soft.assert_equal(teacher_stats.min, expected_min, "Min mismatch")
        soft.assert_equal(teacher_stats.max, expected_max, "Max mismatch")
        soft.assert_equal(round(teacher_stats.avg, 2), expected_avg, "Avg mismatch")

        soft.assert_all()
