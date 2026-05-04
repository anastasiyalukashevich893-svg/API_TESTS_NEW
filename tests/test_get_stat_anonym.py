import random
import requests.status_codes
from faker import Faker
from services.university.helpers.grade_helper import GradeHelper

faker = Faker()


class TestGradeStatAnonym:
    def test_get_stat_anonym(self, university_api_utils_anonym):
        grade_helper = GradeHelper(api_utils=university_api_utils_anonym)
        response = grade_helper.get_stat(student_id=random.randint(1, 99),
                                         teacher_id=random.randint(1, 99),
                                         group_id=random.randint(1, 99))

        assert response.status_code == requests.codes.forbidden, \
            (f"Wrong status code. Actual :'{response.status_code}',"
             f" but expected: '{requests.codes.forbidden}'")
