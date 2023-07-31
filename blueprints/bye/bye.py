from flask import Blueprint, render_template, redirect, url_for

bye = Blueprint("bye", __name__, template_folder="templates")

@bye.route("/")
def index():
    return "Hasla la vista baby!"

@bye.route("/suma/<int:num1>/<int:num2>")
def add(num1, num2):
    return str(num1 + num2)

@bye.route("/adios")
def adios():
    return "ADIOS Hasla la vista baby!"

@bye.route("/go_to_hello")
def go_to_hello():
    return redirect(url_for("helloword.hello_html"))