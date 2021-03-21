from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from data import db_session
from data.users import User
from data.questions import Question
import datetime
from flask import Flask, redirect, render_template
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, RadioField
from wtforms.validators import DataRequired


class RegFrom(FlaskForm):
    email = StringField('Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    repeat_password = PasswordField('Повторите пароль', validators=[DataRequired()])
    username = StringField('Имя пользователя', validators=[DataRequired()])
    submit = SubmitField('Зарегистрироваться')


class LoginForm(FlaskForm):
    email = StringField('Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')


class QuestionForm(FlaskForm):
    text = TextAreaField('Вопрос', validators=[DataRequired()])
    personal = BooleanField('Личное')
    priority = RadioField('Выберите срочность', choices=[('green', 'Не срочно'), ('yellow', 'Cрочно'), ('red', 'Oчень срочно')])
    submit = SubmitField('Задать вопрос')


class AnswerForm(FlaskForm):
    answer = TextAreaField('Ваш ответ')
    submit = SubmitField('Отправить ответ')


app = Flask(__name__)
app.config['PERMANENT_SESSION_LIFETIME'] = datetime.timedelta(
    days=365
)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

login_manager = LoginManager()
login_manager.init_app(app)


@login_required
@app.route('/index')
def index():
    db_session.global_init("db/blogs.db")
    db_sess = db_session.create_session()
    all_users = db_sess.query(User).all()
    all_quests = db_sess.query(Question).all()
    return render_template('index.html', quests=all_quests, all_users=all_users)


@login_manager.user_loader
def load_user(user_id):
    db_session.global_init("db/blogs.db")
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


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
            return redirect("/profile")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@login_required
@app.route('/question', methods=['GET', 'POST'])
def new_question():
    form = QuestionForm()
    if form.validate_on_submit():
        db_session.global_init("db/blogs.db")
        db_sess = db_session.create_session()
        question = Question()
        question.text = form.text.data
        question.shorted_text = form.text.data[:20] + '...' if len(form.text.data) > 20 else form.text.data
        question.user_id = current_user.id
        question.author_username = current_user.username
        question.personal = form.personal.data
        question.priority = form.priority.data
        print(question.personal)
        db_sess.add(question)
        db_sess.commit()
        return redirect("/profile")
    return render_template('new_question.html', title='Задать вопрос', form=form)


@login_required
@app.route('/specialist/<id>')
def make_spec(id):
    if current_user.role == 'Admin':
        db_session.global_init("db/blogs.db")
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.id == id).first()
        user.role = 'Specialist'
        db_sess.commit()
        return redirect('/users')
    else:
        return "Недостаточно прав."


@login_required
@app.route('/operator/<id>')
def make_oper(id):
    if current_user.role == 'Admin':
        db_session.global_init("db/blogs.db")
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.id == id).first()
        user.role = 'Operator'
        db_sess.commit()
        return redirect('/users')
    else:
        return "Недостаточно прав."


@login_required
@app.route('/open/<id>')
def open_quest(id):
    db_session.global_init("db/blogs.db")
    db_sess = db_session.create_session()
    question = db_sess.query(Question).filter(Question.id == id).first()
    return render_template('question.html', quest=question)


@login_required
@app.route('/delete/<id>')
def delete_quest(id):
    db_session.global_init("db/blogs.db")
    db_sess = db_session.create_session()
    question = db_sess.query(Question).filter(Question.id == id).first()
    db_sess.delete(question)
    db_sess.commit()
    return redirect('/profile')


@login_required
@app.route('/add_answer/<id>', methods=["GET", "POST"])
def add_answer(id):
    if current_user.role == 'Specialist':
        form = AnswerForm()
        if form.validate_on_submit():
            db_session.global_init("db/blogs.db")
            db_sess = db_session.create_session()
            question = db_sess.query(Question).filter(Question.id == id).first()
            question.answer_author = current_user.username
            question.answer = form.answer.data
            question.answered = True
            db_sess.commit()
            return redirect('/index')
        db_session.global_init("db/blogs.db")
        db_sess = db_session.create_session()
        question = db_sess.query(Question).filter(Question.id == id).first()
        return render_template('add_answer.html', quest=question, form=form)
    else:
        return redirect('/index')


@login_required
@app.route('/users')
def users():
    if current_user.role == 'Admin':
        db_session.global_init("db/blogs.db")
        db_sess = db_session.create_session()
        all_users = db_sess.query(User).all()
        return render_template('users.html', all_users=all_users)
    else:
        return redirect('/index')


@login_required
@app.route('/profile')
def profile():
    if current_user.role == 'Operator':
        db_session.global_init("db/blogs.db")
        db_sess = db_session.create_session()
        all_quests = db_sess.query(Question).all()
        return render_template('profile.html', quests=all_quests)
    else:
        return redirect('/index')


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')
