import io
import re
import zipfile
import time

import requests
from lxml.html import document_fromstring

from var import dev, env, product, test


def write_to_html(text):
	with open("html.txt", "w") as w:
		w.write(text)

def write_urls_one_page(urls, page, _type):
	_path_file = "./download/{0}/{1}.txt".format(_type, page)
	with open(_path_file, "a+") as f:
		format_text = '\n'.join(urls)
		f.writelines(format_text)

def write_downloaded_line(_type, link):
	name_file = env.downloaded_file.get(_type, None)
	path_file = env.logs_path_dir + name_file
	with open(path_file, "a+") as f:
		f.write('\n' + link)

def read_html_file():
	with open("html.txt", "r") as r:
		_html = r.read()	
	return _html

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
	
	return _rs

def download_file(url, type_folder, folder_name):
	with requests.get(url, proxies = proxies,stream=True) as r:
		assert r.status_code == 200
		z = zipfile.ZipFile(io.BytesIO(r.content))
		z.extractall('./download/{0}/{1}'.format(type_folder, folder_name))

def download_a_url(url, type_folder):
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
		write_downloaded_line(type_folder, url_to_download)
	except Exception as e:
		print("#######EXCEPTION########### download_a_url")
		print(e)
		time.sleep(2)
		download_a_url(url, type_folder)

