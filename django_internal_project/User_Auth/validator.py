from cerberus import Validator

def verifying_signup_request(request):
    # Define the validation schema
    schema = {
        'password': {'type': 'string', 'required': True},
        'username': {'type': 'string', 'required': True},
        'email': {'type': 'string', 'required': False, 'regex': r'^\S+@\S+\.\S+$'},
        'security_q': {'type': 'string', 'required': True},
        'security_a': {'type': 'string', 'required': True}
    }
    v = Validator(schema)
    if v.validate(request.data):
        return True
    else:
        return False


def verifying_user_login(request):
    # Define the validation schema
    schema = {

         'password': {'type': 'string', 'required': True},

    }
    if "username" in request.data:
        schema.update({'username': {'type': 'string', 'required': True}})
    else:
        schema.update({'email': {'type': 'string', 'required': True, 'regex': r'^\S+@\S+\.\S+$'}})
    v = Validator(schema)

    if v.validate(request.data):
        return True
    else:
        return False

def verifying_forgotpassword_request(request):

    schema = {

        'security_a': {'type': 'string', 'required': True},
        'security_q': {'type': 'string', 'required': False},
    }
    if 'username' in request.data :
        schema.update({
            'username': {'type': 'string', 'required': True},

            'new_password': {'type': 'string',  'required': True},
        })

    else:
        schema.update({
            'email': {'type': 'string', 'maxlength': 254, 'required': True},
            'security_q': {'type': 'string', 'required': True},
            'security_a': {'type': 'string', 'required': True},
        })


    v = Validator(schema)
    if v.validate(request.data):
        return True
    else:
        return False


def verifying_resetpassword_request(request):

    schema = {
        'old_password': {'type': 'string', 'required': True},
    }
    if 'username' in request.data :
        schema.update({
            'username': {'type': 'string', 'required': True},
            'new_password': {'type': 'string',  'required': True},
        })

    else:
        schema.update({
            'email': {'type': 'string', 'maxlength': 254, 'required': True},

        })



    v = Validator(schema)
    if v.validate(request.data):
        return True
    else:
        return False


def verifying_refresh_token(request):
    schema = {
        "refresh_token": {'type': 'string', 'required': True}
    }
    v = Validator()
    if v.validate(request.data,schema):
        return True
    else:
        return False




