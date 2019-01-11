import send_request.py as api
from  var import product

#api.get_urls_img()
number_page = product.number_page["psd"]
__type = "psd"

for page in range(1, number_page + 1):
	api.download_one_page(page,__type)