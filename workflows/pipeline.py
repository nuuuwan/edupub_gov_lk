from workflows import download, pdf_to_txt, update_readme


def main():
    download.main()
    pdf_to_txt.main()
    update_readme.main()


if __name__ == '__main__':
    main()
