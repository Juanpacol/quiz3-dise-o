import concurrent.futures
from comment import Comment
from filter import Filter


class ModerationChain:
    def __init__(self, filters: list, parallel: bool = False):
        self.filters = filters
        self.parallel = parallel
        self._build_chain()

    def _build_chain(self):
        for i in range(len(self.filters) - 1):
            self.filters[i].set_next(self.filters[i + 1])
        if self.filters:
            self.filters[-1].next_filter = None

    def moderate(self, comment: Comment) -> Comment:
        if self.parallel:
            return self._moderate_parallel(comment)
        return self.filters[0].handle(comment) if self.filters else comment

    def _moderate_parallel(self, comment: Comment) -> Comment:
        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = [
                executor.submit(f.handle, Comment(text=comment.text))
                for f in self.filters
            ]
            results = [
                f.result() for f in concurrent.futures.as_completed(futures)
            ]

        for result in results:
            if result.blocked:
                comment.blocked = True
            if result.modified:
                comment.modified = True
                comment.text = result.text
            if result.flagged:
                comment.flagged = True
            comment.reasons.extend(result.reasons)

        return comment