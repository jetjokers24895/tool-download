import os

from time import sleep

from download_fotos import download_fotos_v2
from download_psd import download_psd_v2
from download_vectores import download_vectores_v2
from var import env, product


def check_pre():
    dirs = {
        "download": "{0}/download".format(env.WORKING_DIR),

        "download_fotos": "{0}/download/fotos".format(env.WORKING_DIR),
        "download_psd": "{0}/download/psd".format(env.WORKING_DIR),
        "download_vectores": "{0}/download/vectores".format(env.WORKING_DIR),

        "download_fotos_page": "{0}/download/fotos/page".format(env.WORKING_DIR),
        "download_psd_page": "{0}/download/psd/page".format(env.WORKING_DIR),
        "download_vectores_page": "{0}/download/vectores/page".format(env.WORKING_DIR),

    }

    for _dir in dirs.values():
        _ck = os.path.isdir(_dir)

        if not _ck:
            os.makedirs(_dir)


try:
    check_pre()
    for page in range(1, 37986):
        download_fotos_v2(page)
        download_psd_v2(page)
        download_vectores_v2(page)
except Exception as e:
    print("########EXCEPTION############Main")
    print(e)


while 1:
    pass
    sleep(50)