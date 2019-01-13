import os


class product:

    base_url = "https://www.freepik.com/index.php?goto=8&populares=1&page={0}&type={1}"
    type_of_items = [
        # 'iconos',
        'fotos'
        'vectores'
        'psd'

    ]
    number_page = {
        'fotos': 37986,
        'vectores': 31151,
        'psd': 113,
    }


class dev:
    url = "https://www.freepik.com/free-psd"


class env:
    test = False
    base_url_download = "https://download.freepik.com/{0}?lang=en"
    logs_path_dir = './logs/'

    download_dir= './download/'
    downloaded_file = {
        'fotos': 'fotos/downloaded_fotos.txt',
        'vectores': 'vectores/downloaded_vectores.txt',
        'psd': 'psd/downloaded_psd.txt'
    }

    change_network = "{0}/change_ip.exe".format(os.getcwd())
    



class test:
    photo = "https://www.freepik.com/free-photo/golden-silver-christmas-deco-on-black_3239044.htm"
