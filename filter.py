from typing import Optional
from comment import Comment


class Filter:
    def __init__(self, name: str):
        self.name = name
        self.next_filter: Optional["Filter"] = None

    def set_next(self, filter: "Filter") -> "Filter":
        self.next_filter = filter
        return filter

    def handle(self, comment: Comment) -> Comment:
        if self.next_filter and not comment.blocked:
            return self.next_filter.handle(comment)
        return comment
