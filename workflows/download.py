from utils import Log

from edupub_gov_lk import RemoteTextBook

N_DOWNLOAD = 10

log = Log('download')


def main():
    rtb_list = RemoteTextBook.list()
    n_rtb_list = len(rtb_list)
    log.info(f'Found {n_rtb_list} remote text books')

    n_updates = 0
    for i_download, rtb in enumerate(random_rtb_list):
        log.info(f'{i_download+1}/{N_DOWNLOAD}) Downloading {rtb.short_name}')
        did_update = rtb.download()
        if did_update:
            n_update += 1
            if n_update >= N_DOWNLOAD:
                break

if __name__ == '__main__':
    main()
