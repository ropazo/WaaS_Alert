"""
    Servidor web en Flask
    Para ejecutarlo usar una ventana cmd o el terminal y escribir:
        flask --debug run

    En pythonanyware queda en:
        https://ranopazo.pythonanywhere.com
"""
from flask import Flask
from flask import url_for
from flask import render_template
from flaskext.markdown import Markdown
import markdown
import os
from pathlib import Path
from jinja2 import Environment, PackageLoader, select_autoescape

app = Flask(__name__)
Markdown(app)


@app.route("/")
def home():
    bootstrap_header = '<title>PPPT2HTML</title> <meta charset="utf-8"> <meta name="viewport" ' \
                       'content="width=device-width, initial-scale=1"> <link rel="stylesheet" ' \
                       'href="https://maxcdn.bootstrapcdn.com/bootstrap/3.4.1/css/bootstrap.min.css"> <script ' \
                       'src="https://ajax.googleapis.com/ajax/libs/jquery/3.5.1/jquery.min.js"></script> <script ' \
                       'src="https://maxcdn.bootstrapcdn.com/bootstrap/3.4.1/js/bootstrap.min.js"></script> '
    home_template_file = open("templates/home.md", "r", encoding="utf-8")
    home_html = markdown.markdown(
        home_template_file.read()
    )
    return bootstrap_header + home_html


@app.route("/logs")
def get_log():
    bootstrap_header = '<title>PPPT2HTML</title> <meta charset="utf-8"> <meta name="viewport" ' \
                       'content="width=device-width, initial-scale=1"> <link rel="stylesheet" ' \
                       'href="https://maxcdn.bootstrapcdn.com/bootstrap/3.4.1/css/bootstrap.min.css"> <script ' \
                       'src="https://ajax.googleapis.com/ajax/libs/jquery/3.5.1/jquery.min.js"></script> <script ' \
                       'src="https://maxcdn.bootstrapcdn.com/bootstrap/3.4.1/js/bootstrap.min.js"></script> '
    log_filename = os.path.join(app.root_path, 'static/logs', 'log.txt')
    template_md_filename = os.path.join(app.root_path, 'templates', 'logs.md')
    template_html_filename = os.path.join(app.root_path, 'templates', 'logs.html')

    with open(log_filename, "r", encoding="utf-8") as log_file:
        print('Preparando visualización de los logs')
        print(f'Leyendo archivo de logs {log_filename}')
        log_text = log_file.readlines()

    env = Environment(
        loader=PackageLoader(__name__),
        autoescape=select_autoescape()
    )
    template = env.get_template("logs.html")

    with open(template_md_filename, "r", encoding="utf-8") as template_md_file:
        template_md_str = template_md_file.read()
        template_html_str = markdown.markdown(template_md_str)
        with open(template_html_filename, "w") as template_html_file:
            print('Creando templates html desde templates md:')
            print(f'template_html_filename = {template_html_filename}')
            template_html_file.write(template_html_str)

    template_processed = template.render(log_text=log_text)
    return bootstrap_header + template_processed


@app.route("/WaaSCallbackUrl")
def WaaSCallbackUrl():
    body = (
        "<p>Hola mundo, esto se ve choro</p>"
        "<p>Ahora una segunda línea</p>"
        "<p>Ahora una tercera línea</p>"
    )
    return body


print('URLs disponibles:')
with app.test_request_context():
    print(url_for('home'))
    print(url_for('WaaSCallbackUrl'))
