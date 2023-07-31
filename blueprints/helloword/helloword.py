from flask import Blueprint, render_template, redirect

helloword = Blueprint("helloword", __name__, template_folder="templates")

@helloword.route("/")
def index():
    return "Hello Wordl!"

@helloword.route("/hello")
def hello():
    return "hola desde helloword"

@helloword.route("/hello/<name>")
def hello_name(name):
    return f"Hello {name}"

@helloword.route("/hellohtml")
def hello_html():
    return render_template("hello.html")