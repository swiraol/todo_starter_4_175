def error_for_list_title(title, all_lists):
    for lst in all_lists:
        if lst['title'] == title:
            return "The list title already exists"
    
    if not 1 <= len(title) <= 100:
        return "The title must be between 1 and 100 characters"
    
    return None

def find_list_by_id(list_id, all_lists):
    for lst in all_lists:
        if lst['id'] == list_id:
            return lst 
    
    return None

def delete_list_by_id(list_id, all_lists):
    all_lists[:] = [lst for lst in all_lists if not lst['id'] == list_id]
    return None

def find_todo_by_id(todo_id, todos):
    for todo in todos:
        if todo_id == todo['id']:
            return todo
    return None

def delete_todo_by_id(todo_id, todos):
    return [todo for todo in todos if not todo_id == todo['id']]

def mark_all_completed(todos):
    for todo in todos:
        todo['completed'] = True
    return None
            
def error_for_todo(title):
    if 1 <= len(title) <= 100:
        return None
    else:
        return "Your title must be between 1 and 100 characters long"

def todos_remaining(lst):
    return sum(1 for todo in lst['todos'] if not todo['completed'])  

def is_list_completed(lst):
    return todos_remaining(lst) == 0 and len(lst['todos']) > 0