from flask import Flask
from flask import render_template

app = Flask(__name__)


@app.route('/')
def eredmeny():
    eredmeny = 0
    return render_template('calculator.html', eredmeny=eredmeny)


if __name__ == '__main__':
    app.run()
