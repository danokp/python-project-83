import os
from .database import Urls, Url_checks
from datetime import date
from dotenv import load_dotenv
from flask import Flask, request, render_template, flash, redirect, url_for
from urllib.parse import urlunsplit, urlsplit
from validators.url import url as is_valid_url


app = Flask(__name__)
load_dotenv()
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')


def normalize_url(url):
    scheme, netloc = (
        urlsplit(url).scheme.lower(),
        urlsplit(url).netloc.lower(),
    )
    if netloc.startswith('www.'):
        netloc = netloc[4:]
    return urlunsplit((scheme, netloc, '', '', ''))


@app.route('/')
def homepage():
    return render_template('index.html')


@app.route('/urls', methods=['POST', 'GET'])
def list_pages():
    db_urls = Urls()
    if request.method == 'POST':
        url_user_input = request.form.get('url')
        url = normalize_url(url_user_input)
        if len(url) > 255 or not is_valid_url(url):
            flash('Некорректный URL', category='error')
            if not url_user_input:
                flash('URL обязателен', category='error')
            db_urls.close()
            return render_template(
                'index.html',
                url=url_user_input
            )
        if db_urls.get('name', url):
            flash('Страница уже существует', category='info')
        else:
            flash('Страница успешно добавлена', category='success')
            db_urls.insert(
                url=url,
                date=date.today(),
            )
        id = db_urls.get('name', url)[0]
        db_urls.close()
        return redirect(url_for('analize_page', id=id))
    urls = db_urls.get_columns('id', ('id', 'name'))
    db_urls.close()
    return render_template(
        'urls/index.html',
        urls=urls
    )


@app.route('/urls/<id>')
def analize_page(id):
    db_urls = Urls()
    db_url_checks = Url_checks()
    url = db_urls.get('id', id)
    checks = db_url_checks.get_columns_of_exact_url(id, 'id', ('id', 'created_at'))
    return render_template(
        'urls/id/index.html',
        id=url[0],
        name=url[1],
        date=url[2],
        checks=checks
    )


@app.post('/urls/<id>/checks')
def check_page(id):
    db_url_checks = Url_checks()
    flash('Страница успешно проверена', category='success')
    db_url_checks.insert(
        url_id=id,
        date=date.today(),
    )
    db_url_checks.close()
    return redirect(url_for('analize_page', id=id))
