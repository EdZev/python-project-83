import os
from flask import Flask
from dotenv import load_dotenv
from jinja2 import Environment, PackageLoader, select_autoescape

load_dotenv()
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['DATABASE_URL'] = os.getenv('DATABASE_URL')


env = Environment(
    loader=PackageLoader("page_analyzer"),
    autoescape=select_autoescape(['html'])
)
template = env.get_template('layout.html')


@app.route('/')
def hello():
    return template.render()


if __name__ == '__main__':
    app.run()
