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

def write_downloaded_line(_type, link):
	name_file = env.downloaded_file.get(_type, None)
	path_file = env.logs_path_dir + name_file
	with open(path_file, "a+") as f:
		f.write('\n' + link)

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
	return _rs

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

def download_file(url, type_folder, folder_name):
	proxies = change_proxy()
	print(proxies)
	assert proxies != None
	print('b')
	with requests.get(url, proxies = proxies,stream=True) as r:
		assert r.status_code == 200
		print("a")
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

def get_page_downloaded():
	rs = {}
	types = product.type_of_items
	for _type in types:
		_path_to_open = "{0}number-page-{1}.txt".format(env.logs_path_dir, _type)
		try:
			with open(_path_to_open, 'r') as f:
				rs[_type] = f.read()
		except Exception as e:
			print(_path_to_open + " khong ton tai")
			rs[_type] = 1
	return rs

# print(get_page_downloaded())
# a type has more page, a page has more url
def download_one_page(__type, number_page):
	_url = product.base_url.format(number_page, __type)
	_html = send_request(_url)
	items = get_urls_img(_html)
	for item in items:
		download_a_url(item, __type)

def parse_lst_urls_to_5_cluster(lst_urls):
	_divide = int(len(lst_urls)/5)
	rs = []
	for i in range(1,_divide +1):
		_cluster = lst_urls[5 * i -5 : 5*i]
		rs.append(_cluster)
	_add = lst_urls[_divide * 5 : len(lst_urls)]
	rs.append(_add)
	return rs

def router():
	last_page_downloaded = get_page_downloaded()
	# iter type item
	for _type in product.type_of_items:
		number_page = last_page_downloaded.get(_type)
		all_page = product.number_page.get(_type)
		print("number_page", number_page)
		print("all_page", all_page)
		#iter page
		while number_page < all_page:
			# get urls
			# run main action with url just gotten
			try:
				download_one_page(_type, number_page)
			except Exception as e:
				print("#########Exception####### router")
				print("Cant download page {0} of type {1}".format(number_page, _type))
			finally:
				number_page +=1

#download_one_page('psd', 1)

#test 	parse_lst_urls_to_5_cluster
# ints = [i for i in range(1, 38)]
# print(ints)
# print(parse_lst_urls_to_5_cluster(ints))
	
# main_action(test.photo)

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