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

def split_city_lists(ls):
    """return two city lists, origin and end.

    Given a list, it returns the two lists using two
    keywords to identify blocks.

    """
    assert type(ls) == list
    key_start = 'START'
    key_end = 'END'
    assert ls[0] == key_start
    i_end = ls.index(key_end)
    
    

print list_from_file("city-list.txt")

def write_row_to_file(row, file_name):
    assert type(file_name) == str
    assert type(row) == str
    f = open(file_name, 'a')
    f.write(row + '\n')
    
def write_json_to_file(jso, file_name):
    assert type(file_name) == str
    f = open(file_name, 'w')
    json.dump(jso, f)
    
# print create_html_list("city-list-start",list_from_file("city-list.txt"))

def dict_from_list(list):
    """return a dict from a parsed list.
    'input_list' is a fixed and repetitive structure: 
    [origin, destination, distance, origin, destination, distance, ...]

    """
    def insert_origin(origin):
        if origin not in dict:
            dict[origin] = {}
    def insert_destination(origin, destination, distance):
        if destination not in dict[origin]:
            dict[origin][destination] = distance
    assert len(list) > 0 and len(list) % 3 == 0
    dict = {}
    num = len(list) / 3
    for ind in range(num):
        if ind % 3 == 1:
            origin = list[ind]
            destination = list[ind + 1]
            distance = list[ind + 2]
            insert_origin(origin)
            insert_destination(origin, destination, distance)
    return dict

#~ inp = [u'"Milan, Italy","Trento, Italy",223165', u'"Milan, Italy","Venice, Italy",269451', u'"Milan, Italy","Finale Ligure Savona, Italy",197285', u'"Turin, Italy","Trento, Italy",356812', u'"Turin, Italy","Venice, Italy",403098', u'"Turin, Italy","Finale Ligure Savona, Italy",160435', u'"Busto Arsizio Varese, Italy","Trento, Italy",248262', u'"Busto Arsizio Varese, Italy","Venice, Italy",294549', u'"Busto Arsizio Varese, Italy","Finale Ligure Savona, Italy",224160']
#~ print dict_from_list(inp)

