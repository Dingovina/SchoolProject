from flask import Flask, render_template, redirect
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired
from data import db_session
from data.users import User


class LoginForm(FlaskForm):
    asrt_id = StringField('login', validators=[DataRequired()])
    name = StringField('username', validators=[DataRequired()])
    asrt_pass = PasswordField('password', validators=[DataRequired()])
    submit = SubmitField('Join')


def main():
    db_session.global_init("db/blogs.db")
    db_sess = db_session.create_session()


    app.run()


app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


@app.route('/')
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        return redirect('/success')
    return render_template('login.html', title='Авторизация', form=form)


if __name__ == '__main__':
    main()
    app.run(port=8080, host='127.0.0.1')
