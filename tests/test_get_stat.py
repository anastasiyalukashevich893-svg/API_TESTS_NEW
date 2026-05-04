import random
from faker import Faker

from services.university.models.base_student import DegreeEnum
from services.university.models.base_teacher import SubjectEnum
from services.university.models.grade_request import GradeRequest
from services.university.models.group_request import GroupRequest
from services.university.models.student_request import StudentRequest
from services.university.models.teacher_request import TeacherRequest
from services.university.models.university_service import UniversityService

faker = Faker()


class TestGrade:
    def test_get_stat(self, university_api_utils_admin, create_teacher, create_group, create_student, create_grade):
        university_service = UniversityService(university_api_utils_admin)
        teacher = TeacherRequest(first_name=faker.first_name(),
                                 last_name=faker.last_name(),
                                 subject=random.choice([option for option in SubjectEnum]))
        teacher_response = university_service.create_teacher(teacher_request=teacher)
        group = GroupRequest(name=faker.name())
        group_response = university_service.create_group(group_request=group)
        student = StudentRequest(first_name=faker.first_name(),
                                 last_name=faker.last_name(),
                                 email=faker.email(),
                                 degree=random.choice([option for option in DegreeEnum]),
                                 phone=faker.numerify("+7##########"),
                                 group_id=group_response.id)
        student_response = university_service.create_student(student_request=student)
        grade = GradeRequest(teacher_id=teacher_response.id,
                             student_id=student_response.id,
                             grade=random.randint(0, 5))
        grade_response = university_service.create_grade(grade_request=grade)
        assert teacher_response.id == grade_response.teacher_id, (
            f"Wrong teacher id. Actual: '{teacher_response.id}', "
            f"but expected: '{grade_response.teacher_id}'")
        grade_static_response = university_service.get_grade(student_id=student_response.id,
                                                             teacher_id=teacher_response.id,
                                                             group_id=group_response.id)

        assert grade_static_response.count > 0, (
            f"Statistics should not be empty")
