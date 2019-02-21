from app import app
from flask import render_template
from flask_bootstrap import Bootstrap

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')
	
if __name__ == '__main__':
    app.run(debug=True)