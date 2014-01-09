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

def list_from_file(file_name):
    """return the list of lines in a file.

    Given a text file name, return a list
    containing in each element each
    line of the file.

    """
    assert type(file_name) == str
    f = open(file_name, 'r')
    return [line.strip() for line in f]
    
print create_html_list("city-list-start",list_from_file("city-list.txt"))
