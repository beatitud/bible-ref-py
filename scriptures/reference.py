from __future__ import unicode_literals
import re
from scriptures.canons import get_canon


class InvalidReferenceException(Exception):
    """
    Invalid Reference Exception
    """
    pass


class Reference:
    def __init__(self, book=None, chapter=None, verse=None, end_chapter=None, end_verse=None, canon=get_canon()()):
        self.book = book
        self.chapter = chapter
        self.verse = verse
        self.end_chapter = end_chapter
        self.end_verse = end_verse
        self.language = canon.language
        self.canon = canon
        self.book_dict = None
        self.is_valid = None

    def __repr__(self):
        b, c, v, ec, ev = self.book, self.chapter, self.verse, self.end_chapter, self.end_verse
        if not b:
            b = 'Unknown'
            c = '___'
            return '<Ref({0} {1}:{2})>'.format(b, c, v)

        bc = self.book_dict.get('chapters')

        if c == ec and len(bc) == 1:  # single chapter book
            if v == ev:  # single verse
                return '<Ref({0} {1})>'.format(b, v)
            else:  # multiple verses
                return '<Ref({0} {1}-{2})>'.format(b, v, ev)
        else:  # multi chapter book
            if c == ec:  # same start and end chapters
                if v == 1 and ev == bc[c - 1]:  # full chapter
                    return '<Ref({0} {1})>'.format(b, c)
                elif v == ev:  # single verse
                    return '<Ref({0} {1}:{2})>'.format(b, c, v)
                else:  # multiple verses
                    return '<Ref({0} {1}:{2}-{3})>'.format(
                        b, c, v, ev)
            else:  # multiple chapters
                if v == 1 and ev == bc[ec - 1]:  # multi chapter ref
                    return '<Ref({0} {1}-{2})>'.format(b, c, ec)
                else:  # multi-chapter, multi-verse ref
                    return '<Ref({0} {1}:{2}-{3}:{4})>'.format(b, c, v, ec, ev)

    def validate(self, raise_error=True):
        """
        Get a complete five value tuple scripture reference with full book name
        from partial data
        """
        if not self.book_dict:
            if not self.find_book(self.book):
                self.is_valid = False
                if raise_error:
                    raise InvalidReferenceException
                else:
                    return self.is_valid

        # Convert to integers or leave as None
        try:
            self.chapter = int(self.chapter) if self.chapter else None
            self.verse = int(self.verse) if self.verse else None
            self.end_chapter = int(self.end_chapter) if self.end_chapter else self.chapter
            self.end_verse = int(self.end_verse) if self.end_verse else None
        except Exception:
            self.is_valid = False
            if raise_error:
                raise InvalidReferenceException
            else:
                return self.is_valid

        # In case of incomplete or wrong information, we raise an exception
        chapters = self.book_dict.get('chapters')
        chapters_count = len(chapters)
        if (not self.chapter or self.chapter < 1 or self.chapter > chapters_count) \
                or (self.verse and (self.verse < 1 or self.verse > chapters[self.chapter - 1])) \
                or (self.end_chapter and (self.end_chapter < 1 or self.end_chapter < self.chapter or self.end_chapter > chapters_count)) \
                or (self.end_verse and (self.end_verse < 1 or (self.end_chapter and self.end_verse > chapters[self.chapter - 1])
                                        or (self.chapter == self.end_chapter and self.end_verse < self.verse))):
            self.is_valid = False
            if raise_error:
                raise InvalidReferenceException
            else:
                return self.is_valid

        # When there are no values, we set default ones
        if not self.verse:
            self.verse = 1

        if not self.end_verse:
            if self.end_chapter and self.end_chapter != self.chapter:
                self.end_verse = chapters[self.chapter - 1]
            else:
                self.end_verse = self.verse

        if not self.end_chapter:
            self.end_chapter = self.chapter

        self.is_valid = True
        return self.is_valid

    def find_book(self, name):
        """
        Get a book from its name or None if not found
        """
        if not name:
            return None

        for book_dict in self.canon.books.values():
            if re.match('^%s$' % book_dict.get(self.language)[2], name, re.IGNORECASE):
                self.book_dict = book_dict
                self.book = self.book_dict.get(self.language)[0]
                return self.book

        return None

    def is_valid(self,):
        """
        Check to see if a scripture reference is valid
        """
        try:
            return self.validate()
        except InvalidReferenceException:
            return False