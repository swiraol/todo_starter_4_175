from uuid import uuid4

from todos.utils import error_for_list_title, delete_list_by_id, delete_todo_by_id, error_for_todo, find_list_by_id, find_todo_by_id, mark_all_completed, todos_remaining

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
    return render_template('lists.html', lists=session['lists'], todos_remaining=todos_remaining)

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

@app.route('/lists/<list_id>', methods=['POST'])
def update_list(list_id):
    lst = find_list_by_id(list_id, session['lists'])
    if not lst:
        raise NotFound(description="List not found")
    title = request.form['list_title'].strip()
    error = error_for_list_title(title, session['lists'])
    if error:
        flash(error, "error")
        return render_template('edit_list.html', lst=lst, title=title)
    lst['title'] = title 
    session.modified = True 
    flash("The title has been updated", "success")

    return redirect(url_for('show_list', list_id=list_id))

@app.route('/lists/<list_id>/edit')
def edit_list(list_id):
    lst = find_list_by_id(list_id, session['lists'])
    if not lst:
        raise NotFound(description="List not found")
    
    return render_template('edit_list.html', lst=lst)

@app.route('/lists/<list_id>/delete')
def delete_list(list_id):
    lst = find_list_by_id(list_id, session['lists'])
    if not lst:
        raise NotFound(description="List not found")
    
    delete_list_by_id(list_id, session['lists'])
    session.modified = True 
    flash("The list has been deleted", "success")

    return redirect(url_for('get_lists'))
    
@app.route('/lists/<list_id>/complete_all', methods=['POST'])
def mark_all_todos_completed(list_id):
    lst = find_list_by_id(list_id, session['lists'])
    if not lst:
        raise NotFound(description="List not found")
    mark_all_completed(lst['todos'])
    session.modified = True 
    flash('All todos have been completed', 'success')
    return redirect(url_for('show_list', list_id=list_id))

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

@app.route('/lists/<list_id>/todos/<todo_id>/toggle', methods=["POST"])
def update_todo_status(list_id, todo_id):
    lst = find_list_by_id(list_id, session['lists'])
    if not lst:
        raise NotFound(description="List not found")
    
    todo = find_todo_by_id(todo_id, lst['todos'])
    if not todo:
        raise NotFound(description="Todo not found")
    completed = (request.form['completed'] == 'True')
    todo['completed'] = completed
    session.modified = True 
    if completed:
        flash('The todo has been completed', 'success')    
    else:
        flash('The todo is now incomplete', 'success')
    return redirect(url_for('show_list', list_id=list_id))

@app.route('/lists/<list_id>/todos/<todo_id>/delete', methods=['POST'])
def delete_todo(list_id, todo_id):
    lst = find_list_by_id(list_id, session['lists'])
    if not lst:
        raise NotFound(description="List not found")
    
    todo = find_todo_by_id(todo_id, lst['todos'])
    if not todo:
        raise NotFound(description="Todo not found")
    lst['todos'] = delete_todo_by_id(todo_id, lst['todos'])
    session.modified = True
    flash("Todo has been deleted", "success")
    return redirect(url_for('show_list', list_id=list_id))

if __name__ == "__main__":
    app.run(debug=True, port=5003)
    for rule in app.url_map.iter_rules():
        print(rule.methods, rule.rule, '->', rule.endpoint)