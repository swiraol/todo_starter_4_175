def error_for_list_title(title, all_lists):
    for lst in all_lists:
        if lst['title'] == title:
            return "The list title already exists"
    
    if not 1 <= len(title) <= 100:
        return "The title must be between 1 and 100 characters"
    
    return None