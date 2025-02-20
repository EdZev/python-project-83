import os
import requests
from flask import (
    Flask,
    redirect,
    request,
    get_flashed_messages,
    flash,
    url_for
)
from dotenv import load_dotenv
from jinja2 import Environment, PackageLoader, select_autoescape
from page_analyzer.utilities import is_valid_url, normalize_url, get_seo_data
from page_analyzer.url_repository import UrlRepository

load_dotenv()
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['DATABASE_URL'] = os.getenv('DATABASE_URL')
repo = UrlRepository(app.config['DATABASE_URL'])


env = Environment(
    loader=PackageLoader("page_analyzer"),
    autoescape=select_autoescape(['html'])
)


@app.get('/')
def main_page():
    url_data = {}
    template = env.get_template('index.html')
    return template.render(
        url_data=url_data,
        url_for=url_for
    )


@app.get('/urls')
def get_urls():
    urls_list = repo.get_content_urls()
    template = env.get_template('urls.html')
    return template.render(
        urls=urls_list,
        url_for=url_for
    )


@app.get('/urls/<id>')
def get_url(id):
    url_data = repo.find_urls_by_id(id)
    checks_data = repo.get_checks(id)
    messages = get_flashed_messages(with_categories=True)
    template = env.get_template('url.html')
    return template.render(
        url_data=url_data,
        checks_data=checks_data,
        messages=messages,
        url_for=url_for
    )


@app.post('/urls')
def add_new_url():
    url_data = request.form.to_dict()
    validate_url = is_valid_url(url_data['url'])
    if not validate_url:
        errors = [['alert-danger', 'Некорректный URL']]
        template = env.get_template('index.html')
        return template.render(
            url_data=url_data,
            messages=errors,
            url_for=url_for
        ), 422

    normalized_url = normalize_url(url_data['url'])
    url_from_db = repo.find_urls_by_name(normalized_url)
    if url_from_db:
        id = url_from_db['id']
        flash('Страница уже существует', 'alert-info')
    else:
        url_data['url'] = normalized_url
        id = repo.save_urls(url_data)
        flash('Страница успешно добавлена', 'alert-success')
    return redirect(url_for('get_url', id=id), code=302)


@app.post('/urls/<id>/checks')
def check_url(id):
    url = repo.find_urls_by_id(id)['name']
    try:
        r = requests.get(url)
        status_code = r.status_code
        if status_code == requests.codes.ok:
            seo_data = get_seo_data(r.content)
            seo_data['status_code'] = status_code
            repo.save_check_url(id, seo_data)
            flash('Страница успешно проверена', 'alert-success')
    except requests.exceptions.RequestException:
        flash('Произошла ошибка при проверке', 'alert-danger')
    finally:
        return redirect(url_for('get_url', id=id))


if __name__ == '__main__':
    app.run()
