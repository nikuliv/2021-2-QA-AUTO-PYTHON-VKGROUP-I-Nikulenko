import pytest
from utils.data_gen import create_user_name, create_user_phone_number


class MockBase:

    @staticmethod
    def create_user(connect):
        user_name = create_user_name()
        user_number = create_user_phone_number()
        user = {'name': user_name, 'phone_number': user_number}
        response = connect.post('/create_user', user)

        return [user, response]
