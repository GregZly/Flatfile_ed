import os


#from library.read_and_show_csv import app #example of reading and writing
#from library.add_new_row import app #example of writing data to the end of file
from library.modifiable_list import app #example of modifying existing row
#from library.add_and_sort import app #example of adding row with save
if __name__ == '__main__':
    app.debug = True
    host = os.environ.get('IP', '0.0.0.0')
    port = int(os.environ.get('PORT', 8080))
    app.run(host=host,port=port) 