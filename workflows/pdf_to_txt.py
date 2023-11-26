import os
import re

from pdfminer.high_level import extract_text
from utils import File, Log

LINE = '-' * 80
MIN_LINE_LENGTH = 5
log = Log('pdf_to_txt')


def clean_line(line):
    line = re.sub(r'\s+', ' ', line)
    line = line.strip()
    return line


def clean_text(content):
    lines = content.split('\n')
    lines = [clean_line(line) for line in lines]
    lines = [line for line in lines if len(line) >= MIN_LINE_LENGTH]

    found_index = False
    i_index = 0
    for line in lines:
        if line in ['Index', 'Contents', 'CONTENTS']:
            found_index = True
            break
        i_index += 1
    if found_index:
        lines = lines[i_index:]
    return '\n'.join(lines)


def build_txts(force_build=False):
    for file_only in os.listdir(os.path.join('data', 'pdf')):
        if not file_only.endswith('.pdf'):
            continue

        pdf_path = os.path.join('data', 'pdf', file_only)
        txt_path = os.path.join('data', 'txt', file_only + '.txt')

        if os.path.exists(txt_path) and not force_build:
            log.warn(f'{txt_path} Exists')
        else:
            content = extract_text(pdf_path)
            cleaned_content = clean_text(content)
            n_content = len(cleaned_content) / 1_000_000
            File(txt_path).write(cleaned_content)
            log.info(f'Wrote {txt_path} ({n_content:.3f} MB)')


def build_all_txt():
    content_list = []
    for file_only in os.listdir(os.path.join('data', 'txt')):
        if not file_only.endswith('.pdf.txt'):
            continue

        txt_path = os.path.join('data', 'txt', file_only)
        content = File(txt_path).read()
        content_list.extend([LINE, txt_path, LINE, content])

    all_content = '\n'.join(content_list)
    n_all_content = len(all_content) / 1_000_000
    all_text_path = os.path.join('data', 'txt', 'all.txt')
    File(all_text_path).write(all_content)
    log.info(f'Wrote {all_text_path} ({n_all_content:,} MB)')


def main():
    build_txts(force_build=True)
    build_all_txt()


if __name__ == '__main__':
    main()
