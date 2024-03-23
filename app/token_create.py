import uuid


def create_token():
    print(uuid.uuid4())
    return str(uuid.uuid4())
