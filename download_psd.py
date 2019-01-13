
from var import env

if env.test == True:
    import test as api
else:
    import send_request as api

from  var import product

#api.get_urls_img()
number_page = product.number_page["psd"]
__type = "psd"

def download_psd():
	for page in range(1, number_page + 1):
		api.download_one_page(page, __type)

if __name__== "__main__":
	download_psd()