import random

from utils import Log

from edupub_gov_lk import RemoteTextBook

N_DOWNLOAD = 5

log = Log('download')



def main():
    rtb_list = RemoteTextBook.list()
    n_rtb_list = len(rtb_list)
    log.info(f'Found {n_rtb_list} remote text books')
    random.shuffle(rtb_list)
    random_rtb_list = rtb_list[:N_DOWNLOAD]
    for i_download, rtb in enumerate(random_rtb_list):
        log.info(f'{i_download+1}/{N_DOWNLOAD}) Downloading {rtb.short_name}')
        rtb.download()


if __name__ == '__main__':
    main()
