from flask import Flask
from flask_login import LoginManager, login_required

from flask_login_role import role_required, no_role

app = Flask(__name__)
app.config["SECRET_KEY"] = "secret-key"
# LoginManager needs the `no_role` method to redirect users without role privileges.
LoginManager.no_role = no_role
login_manager = LoginManager(app)
login_manager.login_view = "login"
login_manager.no_role_view = "no-role"


# You can demo the @role_required functionality by running this flask app with
# different demo users. Uncomment a user and try to access the views below.
from sample.demo_users import BasicUser, RoleUser, UnauthorizedUser

# user = UnauthorizedUser()
# user = BasicUser()
user = RoleUser()


@app.route("/")
def index():
    return "Anyone can visit this page."


@app.route("/user-page/")
@login_required
def user_page():
    return "Any logged-in users can visit this page."


@app.route("/role-page/")
@login_required
@role_required(["ROLE"])
def role_page():
    return "Only logged-in role users can visit this page."


@app.route("/login/")
def login():
    return "Login page. Unauthorized users requesting @login_required or\
            @role_required pages are redirected here."


@app.route("/no-role/")
@login_required
def no_role():
    return "Authorized users without role privileges are redirected here.<br>\
            Notice that this view can be @login_required, because only users\
            who are authorized but who don't have role privileges will be\
            redirected here.<br>\
            Unauthorized users accessing an @role_required view are redirected\
            to the login_view, so a @login_required decorator is not\
            additionally needed on a @role_required view."


# DO NOT INCLUDE THIS IN YOUR FLASK APP
# This overrides the LoginManager's functionality and is only for demo purposes.
import flask_login.utils as utils


def force_user():
    return user


utils._get_user = force_user
