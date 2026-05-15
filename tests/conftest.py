import random

import pytest
from faker import Faker

from services.auth.models.auth_service import AuthService
from services.auth.models.login_request import LoginRequest
from services.auth.models.register_request import RegisterRequest
from services.university.models.base_grade import MinMaxGrade
from services.university.models.base_student import DegreeEnum
from services.university.models.base_teacher import SubjectEnum
from services.university.models.grade_request import GradeRequest
from services.university.models.group_request import GroupRequest
from services.university.models.student_request import StudentRequest
from services.university.models.teacher_request import TeacherRequest
from services.university.models.university_service import UniversityService
from utils.api_utils import ApiUtils

faker = Faker()


@pytest.fixture(scope="function", autouse=False)
def auth_api_utils_anonym():
    api_utils = ApiUtils(url=AuthService.SERVICE_URL)
    return api_utils


@pytest.fixture(scope="function", autouse=False)
def university_api_utils_anonym():
    api_utils = ApiUtils(url=UniversityService.SERVICE_URL)
    return api_utils


@pytest.fixture(scope="function", autouse=False)
def registered_user(auth_api_utils_anonym):
    auth_service = AuthService(auth_api_utils_anonym)
    username = faker.user_name()
    password = faker.password(
        length=15, special_chars=True, digits=True, upper_case=True, lower_case=True
    )
    email = faker.email()
    auth_service.register_user(
        register_request=RegisterRequest(
            username=username, password=password, password_repeat=password, email=email
        )
    )
    login_response = auth_service.login_user(
        login_request=LoginRequest(username=username, password=password)
    )
    return {
        "username": username,
        "password": password,
        "email": email,
        "access_token": login_response.access_token,
        "token_type": login_response.token_type,
    }


@pytest.fixture(scope="function", autouse=False)
def access_token(registered_user):
    return registered_user["access_token"]


@pytest.fixture(scope="function", autouse=False)
def auth_api_utils_admin(access_token):
    api_utils = ApiUtils(
        url=AuthService.SERVICE_URL, headers={"Authorization": f"Bearer {access_token}"}
    )
    return api_utils


@pytest.fixture(scope="function", autouse=False)
def university_api_utils_admin(access_token):
    api_utils = ApiUtils(
        url=UniversityService.SERVICE_URL, headers={"Authorization": f"Bearer {access_token}"}
    )
    return api_utils


@pytest.fixture(scope="function", autouse=False)
def create_teacher(university_api_utils_admin):
    university_service_teacher = UniversityService(university_api_utils_admin)
    teacher = TeacherRequest(
        first_name=faker.first_name(),
        last_name=faker.last_name(),
        subject=random.choice(list(SubjectEnum)),
    )
    teacher_response = university_service_teacher.create_teacher(teacher_request=teacher)
    return teacher_response


@pytest.fixture(scope="function", autouse=False)
def create_group(university_api_utils_admin):
    university_service_group = UniversityService(university_api_utils_admin)
    group = GroupRequest(name=faker.name())
    group_response = university_service_group.create_group(group_request=group)
    return group_response


@pytest.fixture(scope="function", autouse=False)
def create_student(university_api_utils_admin, create_group):
    university_service_student = UniversityService(university_api_utils_admin)
    student = StudentRequest(
        first_name=faker.first_name(),
        last_name=faker.last_name(),
        email=faker.email(),
        degree=random.choice(list(DegreeEnum)),
        phone=faker.numerify("+7##########"),
        group_id=create_group.id,
    )
    student_response = university_service_student.create_student(student_request=student)
    return student_response


@pytest.fixture(scope="function", autouse=False)
def create_grade(university_api_utils_admin, create_teacher, create_student):
    university_service = UniversityService(university_api_utils_admin)
    grade_value = random.randint(MinMaxGrade.MIN_GRADE, MinMaxGrade.MAX_GRADE)
    grade_response = university_service.create_grade(
        GradeRequest(teacher_id=create_teacher.id, student_id=create_student.id, grade=grade_value)
    )
    return grade_response


@pytest.fixture(scope="function")
def student_factory(university_api_utils_admin, create_group):
    def _create_student():
        university_service = UniversityService(university_api_utils_admin)
        student = StudentRequest(
            first_name=faker.first_name(),
            last_name=faker.last_name(),
            email=faker.email(),
            degree=random.choice(list(DegreeEnum)),
            phone=faker.numerify("+7##########"),
            group_id=create_group.id,
        )
        return university_service.create_student(student_request=student)

    return _create_student
