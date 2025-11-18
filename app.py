from uuid import uuid4

from todos.utils import error_for_list_title, error_for_todo, find_list_by_id

from werkzeug.exceptions import NotFound

from flask import (
    flash,
    Flask, 
    render_template, 
    redirect,  
    request, 
    session,
    url_for,
)

app = Flask(__name__)

app.secret_key = 'secret1'

@app.before_request
def initialize_session():
    if 'lists' not in session:
        session['lists'] = []


@app.route("/")
def index():
    return redirect(url_for('get_lists'))

@app.route("/lists")
def get_lists():
    return render_template('lists.html', lists=session['lists'])

@app.route("/lists", methods=["POST"])
def create_list():
    title = request.form['list_title'].strip()
    error = error_for_list_title(title, session['lists'])
    if error: 
        flash(error, 'error')
        return render_template('new_list.html', title=title)
    session['lists'].append({"id": str(uuid4()), "title": title, "todos": [],})
    session.modified = True
    flash("The list has been added", "success")
    return redirect(url_for('get_lists'))

@app.route('/lists/new')
def add_todo_list():
    return render_template('new_list.html')

@app.route('/lists/<list_id>')
def show_list(list_id):
    lst = find_list_by_id(list_id, session['lists'])
    if lst: 
        return render_template('list.html', lst=lst)
    else:
        raise NotFound(description="List not found")

@app.route('/lists/<list_id>/todos', methods=['GET', 'POST'])
def create_new_todo(list_id):
    if request.method == 'POST':
        title = request.form['todo'].strip()
        lst = find_list_by_id(list_id, session['lists'])
        if not lst: 
            raise NotFound(description="List not found")
        
        error = error_for_todo(title)
        if error:
            flash(error, 'error')
            return render_template('list.html', lst=lst)
        
        lst['todos'].append({
            'id': str(uuid4()),
            'title': title,
            'completed': False,
        })
        session.modified = True
        flash("Your todo has been created", "success")
        return redirect(url_for('show_list', list_id=list_id))
    
    lst = find_list_by_id(list_id, session['lists'])
    if not lst: 
        raise NotFound(description="List not found")
    return redirect(url_for('show_list', list_id=list_id))

if __name__ == "__main__":
    app.run(debug=True, port=5003)