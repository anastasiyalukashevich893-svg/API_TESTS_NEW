import requests
from faker import Faker
from services.auth.helpers.authorization_helper import AuthorizationHelper

faker = Faker()


class TestAuthContract:
    def test_auth(self, auth_api_utils_anonym):
        password = "Aq143%!" + faker.word()
        auth_helper = AuthorizationHelper(api_utils=auth_api_utils_anonym)
        register_response = auth_helper.post_register(data={"username": faker.user_name(),
                                                            "password": password,
                                                            "password_repeat": password,
                                                            "email": faker.email()})
        assert register_response.status_code == requests.codes.created, \
            (f"Wrong status code. Actual :'{register_response.status_code}',"
             f" but expected: '{requests.codes.created}'")

    def test_login(self, auth_api_utils_anonym, registered_user):
        auth_helper = AuthorizationHelper(api_utils=auth_api_utils_anonym)
        login_response = auth_helper.post_login(data={"username": registered_user["username"],
                                                      "password": registered_user["password"]})
        assert login_response.status_code == requests.codes.ok, \
            (f"Wrong status code. Actual :'{login_response.status_code}',"
             f" but expected: '{requests.codes.ok}'")
        response_data = login_response.json()
        assert response_data["token_type"] == "Bearer", \
            f"Wrong token_type. Expected 'Bearer', got '{response_data.get('token_type')}'"
        assert "access_token" in response_data, "Response missing 'access_token' field"
