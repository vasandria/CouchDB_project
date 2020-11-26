from flask import Flask, render_template, request, redirect
from jinja2 import Environment, FileSystemLoader, select_autoescape, Template
import couchdb
import os

couch = couchdb.Server('http://vasandria:tabvrf@localhost:5984')
db = couch['todolist']

env = Environment(
    loader=FileSystemLoader('.'),
    autoescape=select_autoescape(['html', 'xml'])
)


def refresh_list(status):
    l = []
    for row in db.view('_all_docs', include_docs=True):
        if row.doc.get('status') == status:
            l.append(row.doc.get('task'))
    return l


def get_id(status):
    l = []
    for row in db.view('_all_docs', include_docs=True):
        if row.doc.get('status') == status:
            l.append(row.doc.get('task'))
    return l


def refresh_page(template):
    l1 = refresh_list('in process')
    l2 = refresh_list('done')
    return template.render(tasks_procces=l1, tasks_done=l2, )


def refresh_status(task):
    for row in db.view('_all_docs', include_docs=True):
        if row.doc.get('task') == task:
            print(task)
            doc = row.doc
            print(doc)
            doc['status'] = "done"
            db.save(doc)


def delete(task):
    for row in db.view('_all_docs', include_docs=True):
        if row.doc.get('task') == task:
            print(task)
            doc = row.doc
            db.delete(doc)


def add_task(task):
    doc1 = {
       'task': task,
       'description': "task",
       'status': "in process"
    }
    db.save(doc1)


app = Flask(__name__)


@app.route('/', methods=['POST', 'GET'])
def hello(name=None):
    template = env.get_template('templates/templates.html')
    rendered_page = refresh_page(template)
    with open('templates/templates.html', 'w', encoding="utf8") as file:
        file.write(rendered_page)
    return rendered_page


@app.route('/add', methods=['POST'])
def add(name=None):
    add_task(request.form.get("name_task"))
    return redirect("/", code=302)


@app.route('/done', methods=['POST'])
def done(name=None):
    refresh_status(request.form.get('task'))
    return redirect("/", code=302)


@app.route('/del', methods=['POST'])
def dell(name=None):
    delete(request.form.get('task'))
    return redirect("/", code=302)


if __name__ == '__main__':
    app.run()
