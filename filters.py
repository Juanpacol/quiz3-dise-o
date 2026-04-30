import re
from filter import Filter
from comment import Comment
from config import SPAM_WORDS, PROFANITY_WORDS


class SpamFilter(Filter):
    SPAM_WORDS = SPAM_WORDS

    def handle(self, comment: Comment) -> Comment:
        for word in self.SPAM_WORDS:
            if word in comment.text.lower():
                comment.blocked = True
                comment.reasons.append(f"{self.name}: contiene palabra spam '{word}'")
                return comment
        return super().handle(comment)


class ProfanityFilter(Filter):
    BAD_WORDS = PROFANITY_WORDS

    def handle(self, comment: Comment) -> Comment:
        modified = False
        for word in self.BAD_WORDS:
            if word in comment.text.lower():
                comment.text = re.sub(word, "*" * len(word), comment.text, flags=re.IGNORECASE)
                modified = True
        if modified:
            comment.modified = True
            comment.reasons.append(f"{self.name}: palabras ofensivas reemplazadas")
        return super().handle(comment)


class LengthFilter(Filter):
    def __init__(self, name: str, max_length: int = 500):
        super().__init__(name)
        self.max_length = max_length

    def handle(self, comment: Comment) -> Comment:
        if len(comment.text) > self.max_length:
            comment.flagged = True
            comment.reasons.append(f"{self.name}: supera {self.max_length} caracteres")
        return super().handle(comment)


class LinkFilter(Filter):
    URL_PATTERN = re.compile(r"https?://\S+")

    def handle(self, comment: Comment) -> Comment:
        links = self.URL_PATTERN.findall(comment.text)
        if links:
            comment.flagged = True
            comment.reasons.append(f"{self.name}: contiene {len(links)} enlaces externos")
        return super().handle(comment)


class CapsFilter(Filter):
    def handle(self, comment: Comment) -> Comment:
        words = comment.text.split()
        caps_words = [w for w in words if w.isalpha() and w.isupper()]
        if caps_words:
            comment.flagged = True
            comment.reasons.append(f"{self.name}: palabras en mayusculas: {caps_words}")
        return super().handle(comment)