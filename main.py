from flask import Flask, render_template, redirect, request
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired
from data import db_session
from data.users import User


class LoginForm(FlaskForm):
    login = StringField('login', validators=[DataRequired()])
    username = StringField('username', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])
    submit = SubmitField('Join')


def main():
    db_session.global_init("db/blogs.db")
    app.run()


app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


@app.route('/', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "GET":
        form = LoginForm()
        return render_template('login.html', title='Авторизация', form=form)
    elif request.method == 'POST':
        db_session.global_init("db/blogs.db")
        db_sess = db_session.create_session()
        user = User
        user.email = request.form['login']
        user.hashed_password = request.form['password']
        user.username = request.form['username']
        print(user)
        db_sess.add(user)
        db_sess.commit()
        return "Форма отправлена"


if __name__ == '__main__':
    main()
    app.run(port=5000, host='127.0.0.1')
