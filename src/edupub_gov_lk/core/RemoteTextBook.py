import os
import re
from dataclasses import dataclass

from utils import Log

from edupub_gov_lk.core.Grade import Grade
from edupub_gov_lk.core.Lang import Lang
from utils_future import WWW

URL_BASE = "http://www.edupub.gov.lk"
log = Log('RemoteTextBook')


@dataclass
class RemoteTextBook:
    lang: Lang
    grade: Grade
    book_id: int
    title_raw: str
    chapter_url_list: list[str]

    @property
    def title_short(self):
        return self.title.replace(' ', '-').lower()

    @property
    def short_name(self):
        return (
            f'{self.lang.short_name}-{self.grade.name_num}-{self.title_short}'
        )

    @property
    def title(self):
        x = self.title_raw
        x = x.replace('-', ' ')
        x = re.sub(r'\s+', ' ', x)
        x = x.strip()
        return x

    def __str__(self):
        return f'RemoteTextBook({self.short_name}))'

    def download(self):
        did_update = False
        for i_chapter, chapter_url in enumerate(self.chapter_url_list):
            file_only = f'{self.short_name}-{i_chapter}.pdf'
            pdf_path = os.path.join('data', file_only)

            if not os.path.exists(pdf_path):
                try:
                    WWW(chapter_url).download_binary(pdf_path)
                    did_update = True
                except BaseException:
                    log.error(f'Failed to download: {pdf_path}')
            else:
                log.warn(f'Already exists: {pdf_path}')

        return did_update

    @staticmethod
    def list_from_lang_and_grade(
        lang: Lang, grade: Grade
    ) -> list['RemoteTextBook']:
        url = URL_BASE + '/SelectSyllabuss.php?'
        soup = WWW(url).get(dict(BookLanguage=lang.id, BookGrade=grade.id))

        a_list = soup.find_all('a', attrs={'class': 'SelectSyllabuss'})
        rtb_list = []
        for a in a_list:
            title = a.text
            book_id = a['bookid']

            url_chapters = URL_BASE + "/SelectChapter.php"
            soup_chapters = WWW(url_chapters).post(
                dict(bookId=book_id),
            )
            a_chapters_list = soup_chapters.find_all(
                'a', attrs={'class': 'SelectChapter'}
            )
            chapter_url_list = []
            for a_chapter in a_chapters_list:
                chapter_url = URL_BASE + '/' + a_chapter['href']
                chapter_url_list.append(chapter_url)

            rtb = RemoteTextBook(
                lang, grade, book_id, title, chapter_url_list
            )
            rtb_list.append(rtb)
            log.debug(str(rtb))
        return rtb_list

    @staticmethod
    def list() -> list['RemoteTextBook']:
        rtb_list = []
        for lang in Lang.list():
            for grade in Grade.list():
                rtb_list.extend(
                    RemoteTextBook.list_from_lang_and_grade(lang, grade)
                )
        sorted_rtb_list = sorted(rtb_list, key=lambda rtb: rtb.book_id)
        return sorted_rtb_list


if __name__ == '__main__':
    RemoteTextBook.list()
