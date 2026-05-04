import requests
import json

from services.general.helpers.base_helper import BaseHelper


class GradeHelper(BaseHelper):
    ENDPOINT_PREFIX = "/grades"
    ROOT_ENDPOINT = f"{ENDPOINT_PREFIX}/"
    STATS_ENDPOINT = f"{ENDPOINT_PREFIX}/stats/"



    def post_grade (self, data: dict)-> requests.Response:
        response = self.api_utils.post(self.ROOT_ENDPOINT, data=data)
        return response

    def get_stat (self, teacher_id = None, student_id = None, group_id = None)-> requests.Response:
        params = {}
        if student_id is not None:
            params["student_id"] = student_id
        if teacher_id is not None:
            params["teacher_id"] = teacher_id
        if group_id is not None:
            params["group_id"] = group_id
        response = self.api_utils.get(self.STATS_ENDPOINT, params=params)
        return response
