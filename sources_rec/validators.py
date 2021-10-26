from rest_framework.exceptions import ValidationError


def validate_source_input(source):
    if not isinstance(source["title"], str) or not isinstance(source["topic"], str) \
            or not isinstance(source["url"], str):
        raise ValidationError
    if not source["title"] or not source["topic"] or not source["url"]:
        raise ValidationError


def validate_get_source_input(source_id):
    if not isinstance(source_id, int):
        raise ValidationError
    if not source_id:
        raise ValidationError


def validate_delete_source_input(source_id):
    if not isinstance(source_id, int):
        raise ValidationError
    if not source_id:
        raise ValidationError


def validate_rating_input(rating):
    if not isinstance(rating["source"], int) or not isinstance(rating["user"], int) \
            or not isinstance(rating["rating"], int):
        raise ValidationError
    if rating["rating"] > 5 or rating["rating"] < 1:
        raise ValidationError


def validate_user_ratings_input(data):
    if not isinstance(data, int):
        raise ValidationError
    if not data:
        raise ValidationError


def validate_delete_rating_input(rating):
    if not isinstance(rating["source"], int) or not isinstance(rating["user"], int):
        raise ValidationError
    if not rating["source"] or not rating["user"]:
        raise ValidationError
