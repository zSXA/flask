from flask import Flask, render_template, session, redirect, url_for, flash
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from flask_sqlalchemy import SQLAlchemy
from wtforms.validators import DataRequired
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from flask_migrate import Migrate

class Base(DeclarativeBase):
	pass

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Трудноугадываемая строка'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost/postgres'
db = SQLAlchemy(model_class=Base)
migrate = Migrate(app, db)
db.init_app(app)
app.config['SQLALCHEMY_COMMIT_TEARDOWN'] = True
bootstrap = Bootstrap(app)
moment = Moment(app)

class Role(Base):
	__tablename__ = 'roles'
	id: Mapped[int] = mapped_column(primary_key=True, autoincrement = True)
	name: Mapped[str] = mapped_column(db.String(64), unique=True)
	users: Mapped[list["User"]] = relationship(back_populates="role")

	def __repr__(self):
		return '<Role %r>' % self.name

class User(Base):
	__tablename__ = 'users'
	id: Mapped[int] = mapped_column(primary_key=True, autoincrement = True)
	username: Mapped[str] = mapped_column(db.String(64), unique=True, index=True)
	role_id: Mapped[int] = mapped_column(db.ForeignKey("roles.id"))
	role: Mapped["Role"] = relationship(back_populates='users')

	def __repr__(self):
		return '<User %r>' % self.username

class NameForm(FlaskForm):
	name = StringField('Как тебя зовут?', validators=[DataRequired()])
	submit = SubmitField('Отправить')

@app.route('/', methods=['GET', 'POST'])
def index():
	name = None
	form = NameForm()
	if form.validate_on_submit():
		user = db.session.execute(db.select(User).filter_by(username=form.name.data)).scalars().first()
		if user is None:
			user_role = db.session.execute(db.select(Role).filter_by(name='User')).scalars().first()
			user = User(username = form.name.data, role=user_role)
			db.session.add(user)
			session['known'] = False
		else:
			session['known'] = True
		session['name'] = form.name.data
		form.name.data = ''
		db.session.commit()
		return redirect(url_for('index'))
	return render_template('index.html', 
	form=form, name=session.get('name'), known=session.get('known', False),
	session=session, type=type(session), current_time=datetime.utcnow())

@app.route('/user/<name>')
def user(name):
	return render_template('user.html', name=name)

@app.errorhandler(404)
def page_not_found(e):
	return '<h1>Так блэт! -_- Страница не найден.</h1>', 404

@app.errorhandler(500)
def internal_server_error(e):
	return 500

if __name__ == '__main__':
	app.run(debug=True)
