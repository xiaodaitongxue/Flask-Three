from flask import Flask, render_template, session, views, request
from flask_session import Session

from redis import Redis
from wtforms import Form, simple, validators, widgets, core
import blue_cbv

app = Flask(__name__)
app.config["DEBUG"]=True
# app.secret_key="asdsf"
app.config["SESSION_TYPE"]="redis"
app.config["SESSION_REDIS"]=Redis(host="127.0.0.1", port=6379,db=5)
app.register_blueprint(blue_cbv.bp)

Session(app)

@app.route('/')
def index():
    return 'Hello World!'
class LoginForm(Form):
    username = simple.StringField(
        label="用户名",
        validators=[
            validators.DataRequired(message='数据不能为空'),
            validators.Length(min=5, max=16, message='大于5小于16')
        ],
        # widget=widgets.TextInput(),
        render_kw={"class":"jinyinwanba"}
    )

    password=simple.PasswordField(
        label="密码",
        validators=[
            validators.DataRequired(message="数据不能为空"),
            validators.Length(min=5, max=16, message="长度大于5小于16"),
            validators.Regexp(regex="\d+", message="密码必须为数字")
        ],
        # widget=widgets.PasswordInput(),
        # render_kw={"class": "jinyinwanba"}
    )

class RegForm(Form):
    hobby_init=[]
    def __init__(self, hobby_list):
        self.hobby_list=hobby_list
        # self.hobby_init = []
        self.init_hobby()
        super(RegForm, self).__init__()

    def init_hobby(self):

        for index,item in enumerate(self.hobby_list):
            self.hobby_init.append([index,item])

    username = simple.StringField(
        label="用户名",
        validators=[
            validators.DataRequired(message='数据不能为空'),
            validators.Length(min=5, max=16, message='大于5小于16')
        ],
        # widget=widgets.TextInput(),
        render_kw={"class": "jinyinwanba"}
    )

    password = simple.PasswordField(
        label="密码",
        validators=[
            validators.DataRequired(message="数据不能为空"),
            validators.Length(min=5, max=16, message="长度大于5小于16"),
            validators.Regexp(regex="\d+", message="密码必须为数字")
        ],
        # widget=widgets.PasswordInput(),
        # render_kw={"class": "jinyinwanba"}
    )
    repassword=simple.PasswordField(
        label="密码",
        validators=[
            validators.DataRequired(message="数据不能为空"),
            validators.EqualTo("password", message="两次密码不一致")
        ],
        # widget=widgets.PasswordInput(),
        # render_kw={"class": "jinyinwanba"}
    )

    gender=core.RadioField(
       label="性别",
        choices=(
            (1,"女",),
            (2,"男",),
            (3,"wnaba",),
        ),
        coerce=int,
        default=3
    )

    hobby=core.SelectMultipleField(
        label="嗜好",
        choices=hobby_init,
        coerce=int,
        default=[2,3]
    )

@app.route("/reg",methods=["GET", "POST"])
def reg():
    if request.method=="GET":
        hobby_list=["cy","hj","bd","xx","hh","jj"]
        regfm=RegForm(hobby_list=hobby_list)
        return render_template("reg.html", fm=regfm)
    else:
        regfm=RegForm(request.form)
        if not regfm.validate():
            return render_template("reg.html", fm=regfm)
        return "注册成功"


class Index(views.MethodView):
    # methods=["POST"]
    #decorators=[war,'nei']
    def get(self):


        # session['user']=' i anm'

        # return session["user"]
        # name,value,domain,path,expires,sameSite,httpOnly,secure
        # sessionid,ei2jip210hc1m3wfv2xudp453w4hb28y,127.0.0.1,/,"Thu, 04 Jun 2020 12:33:10 GMT",Lax,true,false
        loginfm=LoginForm()
        return render_template('index.html', fm=loginfm)
    def post(self):
        # print(request.form.get('username'))
        loginfm = LoginForm(request.form)
        if not loginfm.validate():
            return render_template('index.html', fm=loginfm)
        session["user"]: "I am jinyinwangba"
        return "I am les"
        #
        # return session["user"]
app.add_url_rule("/index", endpoint="class_index", view_func=Index.as_view(name="index"))

# class bpclass(views.MethodView):
#      def get(self):
#          return "blue_get"
# bp.add_url_rule("/blue", endpoint="blue", view_func=bpclass.as_view(name="bpclass"))
if __name__ == '__main__':
    app.run()
