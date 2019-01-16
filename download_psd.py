
from var import product
from var import env

if env.test == True:
    import test as api
else:
    import send_request as api


# api.get_urls_img()
number_page = product.number_page["psd"]
__type = "psd"


def download_psd():
    _logs = read_page_downloaded()
    _page = int(_logs["page"])
    url = _logs["url"]
    for page in range(_page, number_page + 1):
        api.download_one_page(page, __type)


def download_psd_v2(page):
    number_page = product.number_page.get(__type, None)
    assert number_page != None

    if page > number_page:
        return

    __info = read_page_downloaded()
    __page = int(__info["page"])
    __url = __info["url"]

    if page < __page:
        return
    api.download_one_page(page, __type)


def read_page_downloaded():
    path_download_dir = env.download_dir
    path_file = env.downloaded_file.get(__type, None)
    assert path_file != None

    path_to_open = "{0}{1}".format(path_download_dir, path_file)
    _text = get_page(path_to_open)
    if _text == 1 or _text == "1":
        return {"page": 1, "url": ""}

    _info = _text.split("__")
    return {"page": _info[0], "url": _info[1]}


def get_page(path_to_open):

    try:
        with open(path_to_open, 'r') as f:
            _text = f.read()
            if not _text:
                return 1
            return _text  # return  "page-url"
    except Exception as e:
        # if file doesnt exist, create file -> write 0 -> return 0
        print(path_to_open + " khong ton tai")
        print(e)
        print("#######Creating#######")
        with open(path_to_open, "w+") as w:
            w.write("1")
        return 1


if __name__ == "__main__":
    download_psd()
