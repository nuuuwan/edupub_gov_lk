import os

from utils import TIME_FORMAT_TIME, File, Log, Time

log = Log('update_readme')


def main():
    n_textbooks = 0
    for file_only in os.listdir('data'):
        if not file_only.endswith('.pdf'):
            continue
        n_textbooks += 1
    date_str = TIME_FORMAT_TIME.stringify(Time.now())

    readme_lines = [
        '# Educational Publications Department - Sri Lanka',
        'Various text books published at '
        + '[http://www.edupub.gov.lk](http://www.edupub.gov.lk/).',
        '',
        f'*{n_textbooks} textbook chapters as of {date_str}*',
    ]
    File('README.md').write('\n\n'.join(readme_lines))
    log.info('Wrote README.md')


if __name__ == '__main__':
    main()
