import random

import requests
from faker import Faker

from services.university.helpers.teacher_helper import TeacherHelper
from services.university.models.base_teacher import SubjectEnum

faker = Faker()


class TestTeacherCreate:
    def test_teacher_create(self, university_api_utils_admin):
        teacher_helper = TeacherHelper(api_utils=university_api_utils_admin)
        teacher_response = teacher_helper.post_teacher({
            "first_name": faker.first_name(),
            "last_name": faker.last_name(),
            "subject": random.choice(list(SubjectEnum)),
        })

        assert teacher_response.status_code == requests.codes.created, (
            f"Wrong status code. Actual :'{teacher_response.status_code}',"
            f" but expected: '{requests.codes.created}'"
        )
