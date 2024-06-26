from . import (
    SerializerMixin,
    validates,
    re,
    db,
    association_proxy,
    hybrid_property,
    flask_bcrypt,
)

class Topic(db.Model):
    __tablename__ = "topics"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    creator_id = db.Column(db.Integer, db.ForeignKey("users.id")) 
    notes = db.relationship("Note", back_populates="topic", lazy=True)
    course_topics = db.relationship("CourseTopic", back_populates="topic")
    creator = db.relationship("User", back_populates="created_topics")

    users = db.relationship(
        "User",
        secondary="user_topics",
        back_populates="topics",
    )

    courses = db.relationship(
        "Course",
        secondary="course_topics",
        back_populates="topics",
        overlaps="course_topics",
    )
