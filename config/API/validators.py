from rest_framework.serializers import ValidationError


def validate_date_period(date_start, date_end):
    if date_start is None and date_end is None:
        return
    if date_start is None or date_end is None:
        raise ValidationError(
            'Both date_start and date_end must be specified or none of them')
    if date_start > date_end:
        raise ValidationError('date_start must be before date_end')
