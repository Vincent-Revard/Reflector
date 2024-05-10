from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import joinedload, contains_eager
import ipdb

from .. import (
    request,
    NoteSchema,
    Note,
    BaseResource,
    User,
    UserCourse,
    CourseTopic,
    Topic,
    Course,
    db,
    get_instance_by_id,
    ValidationError,
    jwt_required,
)
from flask_jwt_extended import current_user


class NotesIndex(BaseResource):
    model = Note
    schema = NoteSchema()

    @jwt_required()
    def get(self, course_id=None, topic_id=None, note_id=None):
        user_id = current_user.id
        user = db.session.query(User).get(user_id)
        if course_id is not None and topic_id is not None:
            course = db.session.query(Course).get(course_id)
            if course not in user.enrolled_courses:
                return {"message": "User not enrolled in this course"}, 400
            topic = db.session.query(Topic).get(topic_id)
            if topic not in course.topics:
                return {"message": "Topic not associated with this course"}, 400
            notes = (
                Note.query.join(Topic, Note.topic)
                .filter(Note.user_id == user_id, Topic.id == topic_id)
                .options(contains_eager(Note.topic))
                .all()
            )
            notes = [note for note in notes if note.user_id == user_id]
            return {"notes": self.schema.dump(notes, many=True)}, 200
        else:
            notes = Note.query.filter_by(user_id=user_id).all()
            # Check if the user is enrolled in the course associated with each note's topic
            for note in notes:
                if not any(
                    course.id in (course.id for course in user.enrolled_courses)
                    for course in note.topic.courses
                ):
                    return {
                        "message": "User is not enrolled in the course associated with one or more notes"
                    }, 400
            notes = [note for note in notes if note.user_id == user_id]
            return {"notes": self.schema.dump(notes, many=True)}, 200

    # @jwt_required()
    # def delete(self, course_id=None, topic_id=None, id=None):
    #     user_id = current_user.id
    #     #
    #     note = get_instance_by_id(Note, id)
    #     if note is None or note.user_id != user_id:
    #         return {"message": "Unauthorized"}, 401
    #     return super().delete(id)

    @jwt_required()
    def patch(self, course_id=None, topic_id=None, id=None):

        note = get_instance_by_id(Note, id)
        if note is None or note.user_id != current_user.id:
            return {"message": "Unauthorized"}, 401
        return super().patch(id)

    @jwt_required()
    def post(self, course_id=None, topic_id=None):
        note_data = request.get_json()
        if not note_data:
            return {"message": "Invalid data"}, 400

        try:
            note = self.schema.load(note_data)
        except ValidationError as err:
            return {"message": "Invalid data", "errors": err.messages}, 400

        user_id = current_user.id

        # Check if the topic is associated with the course
        course_topic = CourseTopic.query.filter_by(
            course_id=course_id, topic_id=topic_id
        ).first()
        if not course_topic:
            return {"message": "Topic not associated with this course"}, 400

        note = Note(user_id=user_id, topic_id=topic_id, **note_data)
        try:
            db.session.add(note)
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            return {"message": "Failed to create note"}, 500

        return {
            "message": "Note created successfully",
            "note": self.schema.dump(note),
        }, 200
