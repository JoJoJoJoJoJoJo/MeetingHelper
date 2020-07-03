from flask import Flask, request, render_template
from flask_bootstrap import Bootstrap
from.forms import FileForm

app = Flask(__name__)
bp = Bootstrap()
bp.init_app(app)


@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)

