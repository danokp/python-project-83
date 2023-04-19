import os
from datetime import date

import requests
from dotenv import load_dotenv
from flask import Flask, flash, redirect, render_template, request, url_for

from .utils import check_url, scrap_web_page
load_dotenv()
from .database import UrlChecks, Urls  # noqa:E402


app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')


@app.route('/')
def homepage():
    return render_template('index.html')


@app.route('/urls')
def list_pages():
    db_url_checks = UrlChecks()
    urls_checks = db_url_checks.join_with_urls()
    return render_template(
        'urls/index.html',
        urls_checks=urls_checks,
    )


@app.post('/urls')
def add_new_page():
    db_urls = Urls()
    url_user_input = request.form.get('url')
    url, errors = check_url(url_user_input)
    if errors:
        for error in errors:
            flash(error, category='error')
        db_urls.close()
        return render_template(
            'index.html',
            url=url_user_input,
        ), 422
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
    return redirect(url_for('analyze_page', id=id))


@app.route('/urls/<int:id>')
def analyze_page(id):
    db_urls = Urls()
    db_url_checks = UrlChecks()
    url = db_urls.get('id', id)
    checks = db_url_checks.get_columns_of_exact_url(
        id,
        'id',
        ('id', 'status_code', 'h1', 'title', 'description', 'created_at'),
    )
    db_url_checks.close()
    return render_template(
        'urls/id/index.html',
        id=url[0],
        name=url[1],
        date=url[2],
        checks=checks,
    )


@app.post('/urls/<int:id>/checks')
def check_page(id):
    db_urls = Urls()
    url_name = db_urls.get('id', id)[1]
    try:
        response = requests.get(url_name)
        response.raise_for_status()
    except requests.exceptions.RequestException:
        flash('Произошла ошибка при проверке', category='error')
        db_urls.close()
        return redirect(url_for('analyze_page', id=id))
    flash('Страница успешно проверена', category='success')
    h1, title, description = scrap_web_page(response)
    status_code = response.status_code
    db_url_checks = UrlChecks()
    db_url_checks.insert(
        url_id=id,
        status_code=status_code,
        date=date.today(),
        h1=h1,
        title=title,
        description=description,
    )
    db_url_checks.close()
    db_urls.close()
    return redirect(url_for('analyze_page', id=id))
