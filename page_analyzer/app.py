import os
from dotenv import load_dotenv
from flask import (
    Flask,
    flash,
    redirect,
    render_template,
    request,
    url_for,
)
import requests

from page_analyzer import db
from page_analyzer.parser import parse_html
from page_analyzer.url import normalize_url, validate_url

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'default-secret-key')


@app.route('/')
def index():
    return render_template('index.html')


@app.post('/urls')
def add_url():
    url_input = request.form.get('url', '').strip()
    errors = validate_url(url_input)

    if errors:
        for error in errors:
            flash(error, 'danger')
        return render_template('index.html', url_value=url_input), 422

    normalized_url = normalize_url(url_input)
    existing_url = db.find_url_by_name(normalized_url)

    if existing_url:
        flash('Страница уже существует', 'info')
        return redirect(url_for('show_url', id=existing_url['id']))

    url_id = db.add_url(normalized_url)
    flash('Страница успешно добавлена', 'success')
    return redirect(url_for('show_url', id=url_id))


@app.get('/urls')
def show_urls():
    urls = db.get_all_urls()
    return render_template('urls/index.html', urls=urls)


@app.get('/urls/<int:id>')
def show_url(id):
    url_record = db.find_url_by_id(id)
    if not url_record:
        flash('Страница не найдена', 'danger')
        return redirect(url_for('show_urls'))

    checks = db.get_url_checks(id)
    return render_template('urls/show.html', url=url_record, checks=checks)


@app.post('/urls/<int:id>/checks')
def create_check(id):
    url_record = db.find_url_by_id(id)
    if not url_record:
        flash('Страница не найдена', 'danger')
        return redirect(url_for('show_urls'))

    try:
        response = requests.get(url_record['name'], timeout=5)
        response.raise_for_status()
    except requests.RequestException:
        flash('Произошла ошибка при проверке', 'danger')
        return redirect(url_for('show_url', id=id))

    parsed_data = parse_html(response.text)

    db.add_url_check(
        id,
        status_code=response.status_code,
        h1=parsed_data['h1'],
        title=parsed_data['title'],
        description=parsed_data['description']
    )

    flash('Страница успешно проверена', 'success')
    return redirect(url_for('show_url', id=id))