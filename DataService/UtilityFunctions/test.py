date = "MyExample2020 Sales"
search_keyword = ["Sales","Purchase"]

def _getIndex(date,search_keyword):
    for word in search_keyword:
        if word in date:
            index_position = date.index(word)
            print(index_position)
            return index_position

index_position = _getIndex(date,search_keyword)
new_string = date[index_position:]
print(new_string)