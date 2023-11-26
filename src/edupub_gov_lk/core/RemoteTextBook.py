import os
import re
from dataclasses import dataclass

from utils import JSONFile, Log

from edupub_gov_lk.core.Grade import Grade
from edupub_gov_lk.core.Lang import Lang
from utils_future import WWW

URL_BASE = "http://www.edupub.gov.lk"
log = Log('RemoteTextBook')

RTB_LIST_PATH = os.path.join('data', 'rtb_list.json')


@dataclass
class RemoteTextBook:
    lang: Lang
    grade: Grade
    book_id: int
    title_raw: str
    chapter_url_list: list[str]

    def to_dict(self):
        return dict(
            lang_id=self.lang.id,
            grade_id=self.grade.id,
            book_id=self.book_id,
            title_raw=self.title_raw,
            chapter_url_list=self.chapter_url_list,
        )

    @staticmethod
    def from_dict(d):
        return RemoteTextBook(
            Lang.from_id(d['lang_id']),
            Grade.from_id(d['grade_id']),
            d['book_id'],
            d['title_raw'],
            d['chapter_url_list'],
        )

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

    def download(self) -> int:
        n_downloads = 0
        for i_chapter, chapter_url in enumerate(self.chapter_url_list):
            file_only = f'{self.short_name}-{i_chapter}.pdf'
            pdf_path = os.path.join('data', 'pdf', file_only)

            if not os.path.exists(pdf_path):
                try:
                    WWW(chapter_url).download_binary(pdf_path)
                    n_downloads += 1
                    log.info(f'Downloaded {chapter_url} to {pdf_path}')
                except BaseException:
                    log.error(f'Failed to download {chapter_url}')
            else:
                log.warn(f'{pdf_path} Exists')

        return n_downloads

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

    @staticmethod
    def store_list():
        rtb_list = RemoteTextBook.list()
        d_list = [rtb.to_dict() for rtb in rtb_list]
        JSONFile(RTB_LIST_PATH).write(d_list)
        log.info(f'Stored {len(rtb_list)} RemoteTextBooks to {RTB_LIST_PATH}')

    @staticmethod
    def list_from_file():
        d_list = JSONFile(RTB_LIST_PATH).read()
        rtb_list = [RemoteTextBook.from_dict(d) for d in d_list]
        log.info(
            f'Loaded {len(rtb_list)} RemoteTextBooks from {RTB_LIST_PATH}'
        )
        return rtb_list
