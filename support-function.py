def create_html_list(title, ilist):
    """ return html code showing the list given.

    Given a list of elements ilist, return an html list,
    - title as <li>
    - every element as <ul>.

    """
    assert type(title) == str
    assert type(ilist) == list
    html = "<li>" + title
    
