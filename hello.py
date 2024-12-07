from flask import Flask, render_template
from flask_bootstrap import Bootstrap
app = Flask(__name__)
bootstrap = Bootstrap(app)

@app.route('/')
def index():
	return render_template('index.html')

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
