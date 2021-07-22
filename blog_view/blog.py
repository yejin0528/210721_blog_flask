from flask import Flask, Blueprint, request, render_template, make_response, jsonify, redirect, url_for, session
from flask_login import login_user, current_user, logout_user
from blog_control.user_mgmt import User
from blog_control.session_mgmt import BlogSession
import datetime

blog_abtest = Blueprint('blog', __name__)


@blog_abtest.route('/set_email', methods=['GET', "POST"])
def set_email():
    if request.method == "GET":
        print('set_email', request.args.get('user_email'))
        return redirect(url_for('blog.test_blog'))
    else:
        print('set_email', request.form['user_email'])
        user = User.create(request.form['user_email'], 'A')
        login_user(user, remember=True, duration=datetime.timedelta(days=365))

        return redirect(url_for('blog.test_blog'))


@blog_abtest.route('/logout')
def logout():
    User.delete(current_user.id)
    logout_user()
    return redirect(url_for('blog.test_blog'))


@blog_abtest.route('/test_blog')
def test_blog():
    if current_user.is_authenticated:  # 구독된 유저이면
        webpage_name = BlogSession.get_blog_page(
            current_user.blog_id)  # return A or B
        BlogSession.save_session_info(
            session['client_id'], current_user.user_email, webpage_name
        )
        return render_template(webpage_name, user_email=current_user.user_email)
    else:
        webpage_name = BlogSession.get_blog_page()  # blog_id = None
        BlogSession.save_session_info(
            session['client_id'], 'anonymous', webpage_name)
        return render_template(webpage_name)
