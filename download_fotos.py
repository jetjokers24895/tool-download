
from var import env, product

if env.test == True:
    import test as api
else:
    import send_request as api


#api.get_urls_img()
number_page = product.number_page["fotos"]
__type = "fotos"

def download_fotos():
	for page in range(1, number_page + 1):
		api.download_one_page(page, __type)


if __name__== "__main__":
	download_fotos()