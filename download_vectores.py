import send_request as api
from var import product

# api.get_urls_img()
number_page = product.number_page["vectores"]
__type = "vectores"

for page in range(1, number_page + 1):
    api.download_one_page(__type, page)
