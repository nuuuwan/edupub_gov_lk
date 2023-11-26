from utils import Log

from edupub_gov_lk import RemoteTextBook

N_DOWNLOAD = 5

log = Log('download')


def main():
    rtb_list = RemoteTextBook.list()
    n_rtb_list = len(rtb_list)
    log.info(f'Found {n_rtb_list} remote text books')

    n_update = 0
    for rtb in rtb_list:
        if rtb.download():
            log.info(f'{n_update+1}/{N_DOWNLOAD}) Updated {rtb.short_name}.')
            n_update += 1
            if n_update >= N_DOWNLOAD:
                break


if __name__ == '__main__':
    main()
