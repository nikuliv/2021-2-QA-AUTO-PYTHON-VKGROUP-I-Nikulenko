from faker import Faker

fake = Faker()


def create_segment_name():
    return fake.bothify(text='segment-???-#########-???-###')
