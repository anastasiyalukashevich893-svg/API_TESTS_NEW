import random
import requests

from services.university.helpers.grade_helper import GradeHelper


class TestCreateGrade:
    def test_create_grade(self, university_api_utils_anonym):
        grade_helper = GradeHelper(api_utils=university_api_utils_anonym)
        response = grade_helper.post_grade({"teacher_id": random.randint(1, 99),
                                            "student_id": random.randint(1, 99),
                                            "grade": random.randint(2, 5)})

        assert response.status_code == requests.codes.forbidden, \
            (f"Wrong status code. Actual :'{response.status_code}',"
             f" but expected: '{requests.codes.forbidden}'")
