"""
    Servidor web en Flask
    Para ejecutarlo usar una ventana cmd o el terminal y escribir:
        flask --debug run

    En pythonanyware queda en:
        https://ranopazo.pythonanywhere.com
"""
from flask import Flask
from flask import request as flask_req
from flaskext.markdown import Markdown
import markdown
import os
import Global
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
    return Global.bootstrap_header + template_processed


@app.route("/log_any/", methods=['GET', 'POST'])
def log_any():
    text = ''
    text += f'base_url\n{flask_req.base_url}</p>'
    text += f'headers\n{flask_req.headers}</p>'
    text += f'data()\n{flask_req.get_data()}</p>'
    text += f'args\n{flask_req.args}</p>'

    return text


@app.route("/WaaSCallbackUrl", methods=['GET', 'POST'])
def waas_callback_url():
    text = flask_req.data.decode("utf-8")
    return 'ini:' + text + ':fin'


