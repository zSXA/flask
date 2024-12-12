from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

class Base(DeclarativeBase):
	pass

db = SQLAlchemy(model_class=Base)
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost/postgres' #'sqlite:///./test.db'
db.init_app(app)


class Test_users(db.Model):
	__tablename__ = 'test_users'
	id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
	username: Mapped[str]
	email: Mapped[str]

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
