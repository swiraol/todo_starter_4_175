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

def find_todo_by_id(todo_id, todos):
    for todo in todos:
        if todo_id == todo['id']:
            return todo
    return None

def delete_todo_by_id(todo_id, todos):
    return [todo for todo in todos if not todo_id == todo['id']]
            
def error_for_todo(title):
    if 1 <= len(title) <= 100:
        return None
    else:
        return "Your title must be between 1 and 100 characters long"