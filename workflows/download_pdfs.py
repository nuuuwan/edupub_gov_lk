from utils import Log

from edupub_gov_lk import RemoteTextBook

MAX_DOWNLOADS = 5

log = Log('download')


def main():
    rtb_list = RemoteTextBook.list_from_file()
    n_all_downloads = 0
    for rtb in rtb_list:
        n_downloads = rtb.download()
        n_all_downloads += n_downloads
        if n_all_downloads >= MAX_DOWNLOADS:
            break


if __name__ == '__main__':
    main()
