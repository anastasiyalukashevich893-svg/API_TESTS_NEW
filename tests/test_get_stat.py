from faker import Faker
from services.university.models.university_service import UniversityService

faker = Faker()


class TestGrade:
    def test_get_stat(self, university_api_utils_admin, create_teacher, create_group, create_student, create_grade):
        university_service = UniversityService(university_api_utils_admin)
        grade_static_response = university_service.get_grade(
            student_id=create_student.id,
            teacher_id=create_teacher.id,
            group_id=create_group.id
        )

        assert grade_static_response.count > 0, (
            f"Statistics should not be empty")
