from db_model.mongodb import conn_mongodb
from datetime import date, datetime


class BlogSession():
    blog_page = {'A': 'blog_A.html', 'B': 'blog_b.html'}  # 사전 데이터
    session_count = 0  # blog A, B 확률 50:50

    @staticmethod
    def save_session_info(session_ip, user_email, webpage_name):
        now = datetime.now()
        now_time = now.strftime("%d/%m/%Y %H:%M:%S")

        mongo_db = conn_mongodb()
        mongo_db.insert_one({
            'session_ip': session_ip,
            'user_email': user_email,
            'page': webpage_name,
            'access_time': now_time
        })

    @staticmethod
    def get_blog_page(blog_id=None):  # blog_id 디폴트 값 None
        if blog_id == None:
            if BlogSession.session_count == 0:
                BlogSession.session_count = 1
                return BlogSession.blog_page['A']
            else:
                BlogSession.session_count = 0
                return BlogSession.blog_page['B']
        else:
            # {'A': 'blog_A.html', 'B': 'blog_b.html'}
            return BlogSession.blog_page[blog_id]
