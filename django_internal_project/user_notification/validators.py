from cerberus import Validator

def validate_notification_data(request):
    schema = {
        'receiver_id': {'type': 'integer', 'required': True},
        'message': {'type': 'string', 'minlength': 1, 'required': True},
        'notification_type': {'type': 'string', 'required': True, 'allowed': ['Friend_Request', 'Message', 'Reminder']},
        'is_read': {'type': 'boolean', 'default': False},
    }
    v = Validator(schema)
    if v.validate(request.data):
        return True
    else:
        return False

