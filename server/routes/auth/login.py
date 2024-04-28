from .. import (
    request,
    Resource,
    User,
    user_schema,
    app,
    create_access_token,
    make_response,
    set_access_cookies,
    create_refresh_token,
    set_refresh_cookies,
    redis_client,
    generate_csrf_token,
    json,
)
import ipdb


class Login(Resource):
    model = User
    schema = user_schema

    def post(self):
        try:
            self.schema.context = {"is_signup": False}
            request_data = request.get_json()
            password = request_data.get("password")
            ipdb.set_trace()
            data = self.schema.load(request_data)
            ipdb.set_trace()
            username = data.username
            # password = request_data.get("password")
            ipdb.set_trace()

            user = User.query.filter_by(username=username).first()
            if user is None or not user.authenticate(password):
                return {"message": "Invalid credentials"}, 401
            access_token = create_access_token(identity=user.id, fresh=True)
            ipdb.set_trace()
            refresh_token = create_refresh_token(identity=user.id)
            csrf_token = generate_csrf_token()
            ipdb.set_trace()
            user_session = {
                "user_id": user.id,
                "access_token": access_token,
                "refresh_token": refresh_token,
                "csrf_token": csrf_token,
            }
            user_session_str = json.dumps(user_session)
            redis_client.set(
                access_token, user_session_str, ex=app.config["JWT_ACCESS_TOKEN_EXPIRES"]
            )
            response = make_response(self.schema.dump(user), 200)
            # response.set_cookie('csrf_token', csrf_token)
            set_access_cookies(response, access_token)
            set_refresh_cookies(response, refresh_token)
            return response
        except Exception as e:
            return {"message": str(e)}, 422
