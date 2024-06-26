from marshmallow import fields, validates, ValidationError
from config import ma
from marshmallow.validate import Length
from email_validator import validate_email, EmailNotValidError

from . import (
    User,
)

class UserSchema(ma.SQLAlchemyAutoSchema):

    class Meta:
        model = User
        load_instance = True  # Optional: deserialize to model instances
        exclude = ("_password_hash",)
    id = fields.Int(dump_only=True)

    username = fields.Str(
        required=True,
        validate=[Length(min=2), Length(max=50)],
        metadata={"description": "The unique username of the user"},
    )
    # password_hash = ma.auto_field("_password_hash", load_only=True, required=True)
    password = fields.Str(load_only=True, required=True, validate=Length(min=8))
    # _password_hash = fields.Str(dump_only=True)
    email = fields.Str(
        metadata={"description": "The email of the user"},
    )
    email_verified = fields.Boolean(  # New field for email verification status
        metadata={"description": "The email verification status of the user"},
    )
    created_courses = fields.Nested(
        "CourseSchema",
        many=True,
        exclude=("creator_id.creator.id", "creator.created.created_courses"),
    )
    created_topics = fields.Nested(
        "TopicSchema",
        many=True,
        exclude=("creator_id.creator.id", "creator.created_topics"),
    )

    @validates("email")
    def validate_email(self, value):
        try:
            v = validate_email(value)
        except EmailNotValidError as e:
            raise ValidationError(str(e))

    @validates("password")
    def validate_password(self, value):
        is_signup = self.context.get("is_signup")
        if is_signup and len(value) < 8:
            raise ValidationError("Password must be at least 8 characters long")

    def load(self, data, instance=None, *, partial=False, **kwargs):

        # Load the instance using Marshmallow's default behavior
        loaded_instance = super().load(
            data, instance=instance, partial=partial, **kwargs
        )
        if "password" in data:
            password = data.pop("password")
            is_signup = self.context.get("is_signup")
            if is_signup:
                # During signup, use the password setter in the User model to hash the password
                loaded_instance.password = password
            else:
                # During login, store the password as is for authentication
                loaded_instance._password_hash = password
            # Put the password back into the data
            data["password"] = password

        # Set attributes manually, triggering property setters
        for key, value in data.items():
            setattr(loaded_instance, key, value)
        print(loaded_instance)
        print(data)
        setattr(loaded_instance, key, value)

        return loaded_instance


#!     do I want a user dictionary instead of object? reference!
# def load(self, data, instance=None, *, partial=False, **kwargs):
#     # Load the instance using Marshmallow's default behavior
#     loaded_instance = super().load(
#         data, instance=instance, partial=partial, **kwargs
#     )

#     if "password" in data:
#         password = data.pop("password")
#         is_signup = self.context.get("is_signup")
#         if is_signup:
#             # During signup, use the password setter in the User model to hash the password
#             loaded_instance.password = password
#         else:
#             # During login, store the password as is for authentication
#             loaded_instance._password_hash = password
#         # Put the password back into the data
#         data["password"] = password

#     # Convert the loaded_instance back to a dictionary
#     data = {c.name: getattr(loaded_instance, c.name) for c in loaded_instance.__table__.columns}

#     return data


UserSchema.notes = fields.Nested("NoteSchema", many=True, exclude=('user_id',))
UserSchema.user_courses = fields.Nested('UserCourseSchema', many=True, exclude=('user_id',))
UserSchema.references = fields.Nested('ReferenceSchema', many=True, exclude=('user_id',))

#! Create schema for a single crew_member
user_schema = UserSchema()
#! Create schema for a collection of crew_members
# * Feel free to use only and exclude to customize
users_schema = UserSchema(many=True)
