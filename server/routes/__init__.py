from functools import wraps
from flask import request, g, render_template, make_response
from flask_restful import Resource
from werkzeug.exceptions import NotFound
# from schemas.crew_member_schema import crew_member_schema, crew_members_schema
# from schemas.production_schema import production_schema, productions_schema
# from schemas.user_schema import user_schema, users_schema
# from models.production import Production
# from models.crew_member import CrewMember
from schemas.userSchema import user_schema, users_schema
import ipdb
from models.user import User
from config import db, app, jwt
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_required,
    get_jwt_identity,
    set_access_cookies,
    set_refresh_cookies,
    unset_jwt_cookies,
    unset_refresh_cookies,
    unset_access_cookies,
    current_user,
    get_jwt,
    verify_jwt_in_request,
    decode_token,
)

#! ==================
#! GENERAL ROUTE CONCERNS
@app.errorhandler(NotFound)
def not_found(error):
    return {"error": error.description}, 404


# @app.before_request
# def before_request():
#     path_dict = {"productionbyid": Production, "crewmemberbyid": CrewMember}
#     if request.endpoint in path_dict:
#         id = request.view_args.get("id")
#         record = db.session.get(path_dict.get(request.endpoint), id)
#         key_name = "prod" if request.endpoint == "productionbyid" else "crew"
#         setattr(g, key_name, record)

def login_required(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        # if "user_id" not in session:
        #     return {"message": "Access Denied, please log in!"}, 422
        return func(*args, **kwargs)

    return decorated_function

# Register a callback function that loads a user from your database whenever
# a protected route is accessed. This should return any python object on a
# successful lookup, or None if the lookup failed for any reason (for example
# if the user has been deleted from the database).
@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    ipdb.set_trace()
    identity = jwt_data["sub"]
    return db.session.get(User, identity)