
from var import env

if env.test == True:
    import test as api
else:
    import send_request as api

from  var import product

# api.get_urls_img()
number_page = product.number_page["vectores"]
__type = "vectores"

def download_vectores():
    _logs = read_page_downloaded()
    page = _logs["page"]
    url = _logs["url"]
    for page in range(page, number_page + 1):
        api.download_one_page(page, __type)

def read_page_downloaded():
    path_download_dir = env.download_dir
    path_file = env.downloaded_file.get(__type, None)
    assert path_file != None

    path_to_open = "{0}{1}".format(path_download_dir, path_file)
    _text = get_page(path_to_open)
    _info = _text.split("-")
    return {"page": _info[0], "url": _info[1]}

def get_page(path_to_open):

    try:
        with open(_path_to_open, 'r') as f:
            return f.read() #return  "page-url"
    except Exception as e:
        # if file doesnt exist, create file -> write 0 -> return 0
        print(_path_to_open + " khong ton tai")
        print(e)
        print("#######Creating#######")
        with open(_path_to_open, "a+") as w:
            w.write(0)
        return 0