from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from data import db_session
from data.users import User
import datetime
from flask import Flask, redirect, render_template
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField, IntegerField
from wtforms.validators import DataRequired, NumberRange


class RegFrom(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    repeat_password = PasswordField('Confirm the password', validators=[DataRequired()])
    username = StringField('Username', validators=[DataRequired()])
    submit = SubmitField('Submit')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember me')
    submit = SubmitField('Login')


class NewCol(FlaskForm):
    column_name = StringField('', validators=[DataRequired(message="?")])
    submit = SubmitField('V')


class NewItem2(FlaskForm):
    summa = IntegerField("", validators=[DataRequired(message="?"),
                                         NumberRange(min=1, message='>0')])
    submit = SubmitField("V")


app = Flask(__name__)
app.config['PERMANENT_SESSION_LIFETIME'] = datetime.timedelta(
    days=365
)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

login_manager = LoginManager()
login_manager.init_app(app)


@app.route('/index/<s>', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
@login_required
def index(s=-1):
    db_session.global_init("db/blogs.db")
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.id == current_user.id).first()
    form = NewItem2()
    form1 = NewCol()
    local_dict = {}
    exec(user.data, globals(), local_dict)
    costs = local_dict["costs"]
    if form.validate_on_submit():
        costs[s].append(int(form.summa.data))
        user.data = "costs = " + str(costs)
        db_sess.commit()
        return redirect("/index")
    if form1.validate_on_submit():
        col_name = form1.column_name.data
        if col_name not in costs and col_name != "new":
            print(123)
            costs[col_name] = []
            user.data = "costs = " + str(costs)
            db_sess.commit()
            return redirect("/index")
        else:
            pass
    max_size = 0
    sums = [sum(s) for s in costs.values()]
    for k, v in costs.items():
        max_size = max(max_size, len(v))
    return render_template('index.html', data=costs, max_size=max_size, sums=sums, status=s, form=form, form1=form1)


@login_manager.user_loader
def load_user(user_id):
    db_session.global_init("db/blogs.db")
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/del/<k>/<i>')
@login_required
def del_item(k, i):
    db_session.global_init("db/blogs.db")
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.id == current_user.id).first()
    local_dict = {}
    exec(user.data, globals(), local_dict)
    costs = local_dict["costs"]
    if k in costs and len(costs[k]) > int(i):
        costs[k].pop(int(i))
    user.data = "costs = " + str(costs)
    db_sess.commit()
    return redirect("/index")


@app.route('/del/<k>')
@login_required
def del_col(k):
    db_session.global_init("db/blogs.db")
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.id == current_user.id).first()
    local_dict = {}
    exec(user.data, globals(), local_dict)
    costs = local_dict["costs"]
    if k in costs:
        del costs[k]
    user.data = "costs = " + str(costs)
    db_sess.commit()
    return redirect("/index")


@app.route('/register', methods=['GET', 'POST'])
def reg():
    form = RegFrom()
    if form.validate_on_submit():
        db_session.global_init("db/blogs.db")
        db_sess = db_session.create_session()
        user = User()
        if form.password.data == form.repeat_password.data:
            try:
                user.email = form.email.data
                user.hashed_password = form.password.data
                user.username = form.username.data
                db_sess.add(user)
                db_sess.commit()
                return redirect('/login')
            except:
                return render_template('registration.html',
                                       message="произошла ошибка (email уже используется, но это не точно)",
                                       form=form)
        return render_template('registration.html',
                               message="пароли не совпадают",
                               form=form)
    return render_template('registration.html', title='Регистрация', form=form)


@app.route('/login', methods=['GET', 'POST'])
@app.route('/', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_session.global_init("db/blogs.db")
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/index/new")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/profile')
@login_required
def profile():
    db_session.global_init("db/blogs.db")
    db_sess = db_session.create_session()
    return render_template('profile.html')


if __name__ == '__main__':
    app.run(port=5050, host='127.0.0.1')
