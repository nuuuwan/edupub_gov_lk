import os

from pdfminer.high_level import extract_text
from utils import File, Log

log = Log('pdf_to_txt')


def main():
    content_list = []
    for file_only in os.listdir('data'):
        if not file_only.endswith('.pdf'):
            continue
        pdf_path = os.path.join('data', file_only)
        txt_path = os.path.join('data-txt', file_only + '.txt')

        if os.path.exists(txt_path):
            log.warn(f'{txt_path} Exists')
            content = File(txt_path).read()
        else:
            content = extract_text(pdf_path)
            n_content = len(content) / 1_000_000
            File(txt_path).write(content)
            log.info(f'Wrote {txt_path} ({n_content:.1f} MB)')

        LINE = '-' * 80
        content_list.extend([LINE, txt_path, LINE, content])

    all_content = '\n'.join(content_list)
    n_all_content = len(all_content) / 1_000_000
    all_text_path = os.path.join('data-txt', 'all.txt')
    File(all_text_path).write(content)
    log.info(f'Wrote {all_text_path} ({n_all_content:.1f} MB)')


if __name__ == '__main__':
    main()
