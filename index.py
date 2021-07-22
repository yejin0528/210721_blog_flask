from flask import Flask, jsonify, request, render_template, make_response, session
from flask_login import LoginManager, current_user, login_manager, login_required, login_user, logout_user
from flask_cors import CORS
from blog_view import blog
from blog_control.user_mgmt import User

app = Flask(__name__, static_url_path="/static")
CORS(app)
app.secret_key = 'dave_server3'  # 시크릿 키

app.register_blueprint(blog.blog_abtest, url_prefix='/blog')
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.session_protection = "strong"


@login_manager.user_loader  # 사용자 객체 다시 로더
def load_user(user_id):
    return User.get(user_id)


@login_manager.unauthorized_handler  # 사용자 로그인 상태 확인
def unauthorized():
    # 401 에러시 success=False 반환
    return make_response(jsonify(success=False), 401)


@app.before_request  # http 연결 처리 전 실행되는 함수
def app_before_request():
    if 'client_id' not in session:
        # request.environ.get : pc 고유의 ip 주소 가져옴
        session['client_id'] = request.environ.get(
            'HTTP_X_REAL_IP', request.remote_addr)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="8081")
