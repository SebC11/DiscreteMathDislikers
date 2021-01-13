import web
from Models import RegisterModel, LoginModel, Posts


web.config.debug = False
urls = (
    '/', 'Home',
    '/register', 'Register',
    '/postregistration', 'PostRegistration',
    '/discover', 'Discover',
    '/profile', 'Profile',
    '/settings', 'Settings',
    '/login', 'Login',
    '/logout', 'Logout',
    '/check-login', 'CheckLogin',
    '/post-activity', 'PostActivity'
)


app = web.application(urls, globals())
session = web.session.Session(app, web.session.DiskStore("sessions"), initializer={'user': None})
session_data = session._initializer

render = web.template.render("Views/Templates", base="MainLayout", globals={'session': session_data, 'current_user': session_data["user"]})



#Classes/Routes
class Home:
    def GET(self):
        # data = type('obj', (object,), {"email" : "test", "password" : "test"})
        #
        # login = LoginModel.LoginModel()
        # isCorrect = login.check_login(data)
        #
        # if isCorrect:
        #     session_data['user'] = isCorrect

        post_model = Posts.Posts()
        posts = post_model.get_all_posts()
        return render.Home(posts)


class Register:
    def GET(self):
        return render.Register()


class Profile:
    def GET(self):
        return render.Profile()


class Settings:
    def GET(self):
        return render.Settings()


class Discover:
    def GET(self):
        return render.Discover()


class PostRegistration:
    def POST(self):
        data = web.input()
        reg_model = RegisterModel.RegisterModel()
        reg_model.insert_user(data)
        return data.email


class CheckLogin:
    def POST(self):
        data = web.input()
        login_model = LoginModel.LoginModel()
        isCorrect = login_model.check_login(data)
        if isCorrect:
            session_data["user"] = isCorrect
            return isCorrect

        return "error"


class Logout:
    def GET(self):
        session['user']= None
        session_data['user'] = None
        session.kill()
        return "success"


class Login:
    def GET(self):
        return render.Login()


class PostActivity:
    def POST(self):
        data = web.input()
        data.username = session_data['user']['username']
        post_model = Posts.Posts()
        post_model.insert_post(data)

        return "success"


if __name__ == "__main__":
    app.run()