def create_html_list(list_id, elements_list):
    """ return html code showing the list given.

    Given a list of elements ilist, return an html list,
    - title as <ul>
    - every element as <li>.

    """
    assert type(list_id) == str
    assert type(elements_list) == list
    html = "<ul id=" + list_id + ">"
    for e in elements_list:
        html += "<li>" + str(e) + "</li>"
    html += "</ul>"
    return html

def import_text_file(file_name):
    """return the content of the file in a string.

    Given a text file name, return a string
    containing the content of the file.

    """
    # TODO
    pass

def create_list_from_string(text):
    """return a list of words contained in the text.

    Given a string text, returns a list of words contained in the text file.

    """
    # TODO
    pass
    
import_text_file("city-list.txt")
