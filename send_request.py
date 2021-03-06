import io
import os
import re
import time
import zipfile
from datetime import datetime

import requests
from lxml.html import document_fromstring

from var import dev, env, product, test


def write_to_html(text):
    with open("html.txt", "w") as w:
        w.write(text)


def read_html_file():
    with open("html.txt", "r") as r:
        _html = r.read()
    return _html


def send_request(url):
    r = requests.get(url)
    assert r.status_code == 200
    return r.text


def filter_premium(divs):
    return [div for div in divs if div.find_class("premium-text") == []]


def get_id_of_item(str_input):
    _id_item = str_input.split("_")
    assert len(_id_item) > 1
    return _id_item[-1].split(".")[0]


def get_name_of_item(str_input):
    return str_input.split("/")[-1].split("_")[0]


def get_urls_img(html):
    doc = document_fromstring(html)
    _divs = doc.find_class("img_box")
    assert len(_divs) > 0
    _divs = filter_premium(_divs)
    _rs = []
    for div in _divs:
        img_div = div.find_class("img-holder")
        assert len(img_div) > 0
        _rs.append(img_div[0].find('a').get('href'))
    print(_rs)
    return sorted(_rs)


def change_proxy():
    r = requests.get("http://pubproxy.com/api/proxy?https=true")
    try:
        _data_json = r.json()['data'][0]
        _ip_port = _data_json['ipPort']
        _proxy = "https://{0}".format(_ip_port)
        proxy_dict = {
            'https': _proxy
        }
        return proxy_dict
    except Exception as e:
        print("######Exception###### change_proxy")
        print("Khong the change proxy")
        print(e)
        return None


def write_fail_link(__type, url):
    path_dir = env.download_dock.get(__type, None)
    assert path_dir != None
    file_dir = "{0}{1}".format(env.logs_path_dir, path_dir)
    with open(file_dir, "a+") as f:
        f.write(url + "\n")


def download_file(url, type_folder, folder_name):
    # proxies = change_proxy()
    # print(proxies)
    # assert proxies != None
    # print('b')
    with requests.get(url, stream=True) as r:
        assert r.status_code == 200
        z = zipfile.ZipFile(io.BytesIO(r.content))
        z.extractall('./download/{0}/{1}'.format(type_folder, folder_name))


def download_a_url(url, type_folder, page_downloading):
    # get name of item
    name_item = get_name_of_item(url)
    assert name_item != None
    # get id of item
    id_item = get_id_of_item(url)
    assert id_item != None
    # download and save to name of item folder
    url_to_download = env.base_url_download.format(id_item)

    try:
        print("downloading {0}".format(url_to_download))
        download_file(url_to_download, type_folder, name_item)
        print("###Downloaded: {0}_{1}".format(name_item, id_item))
        write_downloaded_line(page_downloading, url, type_folder)
        write_downloaded_line_dock(page_downloading, url, type_folder)
    except Exception as e:
        print("#######EXCEPTION########### download_a_url")
        print(e)
        time.sleep(2)
        # write_fail_link(type_folder, url)
        change_ip()
        download_a_url(url, type_folder, page_downloading)


def write_downloaded_line(page, url, __type):
    _path_dir = env.downloaded_file.get(__type, None)
    assert _path_dir != None

    _path_file = "{0}{1}.txt".format(_path_dir, page)
    with open(_path_file, "a+") as w:
        w.write(url + '\n')


def write_downloaded_line_dock(page, url, __type):
    _text = "{0}__{1}".format(page, url)
    path_dir = env.download_dock.get(__type, None)
    assert path_dir != None

    path_file = "{0}{1}".format(env.download_dir, path_dir)
    with open(path_file, "w") as w:
        w.write(_text)


def download_a_cluster(cluster, __type, page_downloading):
    for i in cluster:
        download_a_url(i, __type, page_downloading)


def get_items_one_page(number_page, __type):
    page_downloading = number_page
    _url = product.base_url.format(number_page, __type)
    print(_url)
    _html = send_request(_url)
    items = get_urls_img(_html)
    return items


def download_one_page(number_page, __type):
    items = get_items_one_page(number_page, __type)

    # check urls have not downloaded yet
    items = get_download_dock(__type, items, number_page)

    clusters = parse_lst_urls_to_5_cluster(items)
    # parse to cluster
    for cluster in clusters:
        download_a_cluster(cluster, __type, number_page)
        # run file exe
        change_ip()


def get_info_downloaded(_type, property):
    _path_dir = env.download_dock.get(_type, None)
    assert _path_dir != None

    _path_to_open = "{0}{1}".format(env.download_dir, _path_dir)
    try:
        with open(_path_to_open, 'r') as f:
            __info_downloaded = f.read().split("__")  # return  "page-url"
            __page_downloaded = int(__info_downloaded[0])
            __url = __info_downloaded[1]
            return {"page": __page_downloaded, "url": __url}.get(property, None)

    except Exception as e:
        # if file doesnt exist, create file -> write 0 -> return 0
        print(_path_to_open + " khong ton tai")
        print(e)
        print("#######Creating#######")
        with open(_path_to_open, "w") as w:
            w.write("1")
        return 1


def get_download_dock(__type, items, number_page):
    __page_downloaded = get_info_downloaded(__type, "page")
    __url = get_info_downloaded(__type, "url")

    if __url == 1:
        return items

    assert __page_downloaded != None and __url != None

    if number_page == __page_downloaded:
        try:
            _index = items.index(__url)
            items = items[_index + 1:]
        except ValueError as e:
            print("#########EXCEPTION#### get_download_dock")
            print(e)
            items = get_download_dock_in_exception_case(
                __url, __page_downloaded, __type)

    return items


def find_a_item(url, last_working_page, __type):
    _page = last_working_page

    _page_downloaded = get_info_downloaded(__type, "page")
    assert _page_downloaded != None

    # If the item is deleted, tool will download  next page
    if _page - _page_downloaded == 2:
        return get_items_one_page(_page_downloaded + 1, __type)

    _items = get_items_one_page(last_working_page, __type)
    if _items.count(url) == 0:
        find_a_item(url, _page + 1)  # de quy

    return items


def get_download_dock_in_exception_case(url, last_working_page, __type):
    items = find_a_item(url, last_working_page, __type)
    try:
        _index = items.index(url)
        return items[_index + 1:]
    except Exception as e:
        print("#############EXCEPTION###### get_download_dock_in_exception_case")
        print(e)
        return items


def get_ip():  # get public Ip
    with requests.get('http://ip.42.pl/raw') as r:
        return r.text


def change_ip():
    current_ip = get_ip()
    new_ip = current_ip
    # run changeIp.exe
    os.system(env.change_network)
    start_time = datetime.now()
    wait_change_ip(current_ip, new_ip, start_time)


def wait_change_ip(current_ip, new_ip, since):
    while current_ip == new_ip:
        try:
            time.sleep(15)
            endtime = datetime.now()
            duration = endtime - since
            new_ip = get_ip()

            if duration.seconds > 120:
                change_ip()

        except Exception as e:
            print("######EXCEPTION####### wait_change_ip")
            print(e)
            wait_change_ip(current_ip, new_ip, since)
    print("#######changed_ip###########")


def parse_lst_urls_to_5_cluster(lst_urls):
    _divide = int(len(lst_urls)/5)
    rs = []
    for i in range(1, _divide + 1):
        _cluster = lst_urls[5 * i - 5: 5*i]
        rs.append(_cluster)
    _add = lst_urls[_divide * 5: len(lst_urls)]
    rs.append(_add)
    return rs


def check_new_links(__type):
    # This function to find all new links after downloading in the past
    # To do: example with psd file
        # get the first link of psd (A)
        # get urls in page until urls have the first link
        # iter urls -> find link in urls == A -> only accept link before that

    # get the first link of psd (A)
    first_line = get_first_line(__type)

    # get urls in page until urls have the first link
    links = []
    page = 0
    while not first_line in links:
        page = page + 1
        _links = get_links_one_page(__type, page)
        links.append(_links)

    # iter urls -> find link in urls == A -> only accept link before that
    rs = []
    for link in links:
        if link == first_line:
            break
        rs.append(link)
    return rs


def get_links_one_page(__type, page):
    _url = product.base_url.format(page, __type)
    _html = send_request(_url)
    links = get_urls_img(_html)
    return links


def get_first_line(__type):
    path_dir = env.download_dock.get(__type, None)
    assert path_dir != None
    path_file = "{0}{1}".format(env.logs_path_dir, path_dir)
    with open(path_file, "r") as f:
        first_line = f.readlines()[0].replace("\n", "")
    return first_line

# html = send_request(dev.url)
# write_to_html(html)
# try:
# 	# url = "https://download.freepik.com/3361877?lang=en"
# 	# download_file(url,"test")
# 	type_img = product.type_of_items[0]
# 	url = product.base_url.format('1',type_img) # 1 is page number
# 	content = send_request(url)
# 	urls = get_urls_img(content)
# 	print (urls)

# except Exception as e:
# 	print("#######EXCEPTION###########")
# 	print(e)
