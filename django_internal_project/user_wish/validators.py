from cerberus import Validator


def verifying_user_request(request):
    schema = {
        'tag_id': {'type': 'integer', 'required': True},
        'title': {'type': 'string', 'required': True},
        'description': {'type': 'string', 'required': True},
    }
    v = Validator()
    if v.validate(request.data, schema):
        return True
    else:
        return False

def verifying_request(request):
    schema = {
        'title': {'type': 'string', 'required': True},
        'description': {'type': 'string', 'required': True}
    }
    v = Validator()
    if v.validate(request.data, schema):
        return True
    else:
        return False


def verifying_request(request):
    schema = {
        'title': {'type': 'string', 'required': True},
        'description': {'type': 'string', 'required': True}
    }
    v = Validator()
    if v.validate(request.data, schema):
        return True
    else:
        return False

