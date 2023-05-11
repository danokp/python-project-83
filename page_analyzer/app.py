import os
from datetime import date

import requests
from dotenv import load_dotenv
from flask import Flask, flash, redirect, render_template, request, url_for

from .url_processing import check_url
from .web_scraping import scrap_web_page
load_dotenv()
import page_analyzer.database as db  # noqa:E402


app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')


@app.route('/')
def homepage():
    return render_template('index.html')


@app.route('/urls')
def list_pages():
    db_conn, db_cur = db.initiate_conn()
    urls_checks = db.join_urlchecks_with_urls(db_cur)
    db.close_conn(db_conn, db_cur)
    return render_template(
        'urls.html',
        urls_checks=urls_checks,
    )


@app.post('/urls')
def add_new_page():
    url_user_input = request.form.get('url')
    url, errors = check_url(url_user_input)
    if errors:
        for error in errors:
            flash(error, category='error')
        return render_template(
            'index.html',
            url=url_user_input,
        ), 422

    db_conn, db_cur = db.initiate_conn()
    if db.get_from_urls(db_cur, 'name', url):
        flash('Страница уже существует', category='info')
    else:
        flash('Страница успешно добавлена', category='success')
        db.insert_in_urls(
            db_conn,
            db_cur,
            url=url,
            date=date.today(),
        )
    id = db.get_from_urls(db_cur, 'name', url)[0]
    db.close_conn(db_conn, db_cur)
    return redirect(url_for('analyze_page', id=id))


@app.route('/urls/<int:id>')
def analyze_page(id):
    db_conn, db_cur = db.initiate_conn()
    url = db.get_from_urls(db_cur, 'id', id)
    checks = db.get_columns_of_exact_url_from_urlchecks(
        db_cur,
        id,
        'id',
        ('id', 'status_code', 'h1', 'title', 'description', 'created_at'),
    )
    db.close_conn(db_conn, db_cur)
    return render_template(
        'url.html',
        id=url[0],
        name=url[1],
        date=url[2],
        checks=checks,
    )


@app.post('/urls/<int:id>/checks')
def check_page(id):
    db_conn, db_cur = db.initiate_conn()
    url_name = db.get_from_urls(db_cur, 'id', id)[1]
    try:
        response = requests.get(url_name)
        response.raise_for_status()
    except requests.exceptions.RequestException:
        flash('Произошла ошибка при проверке', category='error')
        db.close_conn(db_conn, db_cur)
        return redirect(url_for('analyze_page', id=id))
    flash('Страница успешно проверена', category='success')
    h1, title, description = scrap_web_page(response)
    status_code = response.status_code
    db.insert_in_urlchecks(
        db_conn,
        db_cur,
        url_id=id,
        status_code=status_code,
        date=date.today(),
        h1=h1,
        title=title,
        description=description,
    )
    db.close_conn(db_conn, db_cur)
    return redirect(url_for('analyze_page', id=id))
