from faker import Faker

fake = Faker()


def create_user_name():
    return fake.first_name()


def create_user_phone_number():
    return f'+7{fake.msisdn()[3:]}'
