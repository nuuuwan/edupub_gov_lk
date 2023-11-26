import os
from utils import File, Log
from pdfminer.high_level import extract_text

log = Log('pdf_to_txt')


def main():
    for file_only in os.listdir('data'):
        if not file_only.endswith('.pdf'):
            continue
        pdf_path = os.path.join('data', file_only)
        txt_path = os.path.join('data-txt', file_only + '.txt')

        if os.path.exists(txt_path):
            log.warn(f'{txt_path} Exists')
            continue

        content = extract_text(pdf_path)
        n_content = len(content) / 1_000_000
        File(txt_path).write(content)
        log.info(f'Wrote {txt_path} ({n_content:.1f} MB)')


if __name__ == '__main__':
    main()
