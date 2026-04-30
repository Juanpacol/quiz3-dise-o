import concurrent.futures
from comment import Comment
from filter import Filter


class ModerationChain:
    def __init__(self, filters: list, parallel: bool = False):
        self.filters = filters
        self.parallel = parallel
        self._build_chain()

    def _build_chain(self):
        # Limpia los next_filter de todos antes de reconstruir
        for f in self.filters:
            f.next_filter = None
        for i in range(len(self.filters) - 1):
            self.filters[i].set_next(self.filters[i + 1])

    def add_filter(self, filter: Filter, position: int = None):
        """Agrega un filtro al final o en una posición específica."""
        if position is None:
            self.filters.append(filter)
        else:
            self.filters.insert(position, filter)
        self._build_chain()

    def remove_filter(self, name: str):
        """Elimina un filtro por nombre."""
        self.filters = [f for f in self.filters if f.name != name]
        self._build_chain()

    def reorder(self, names: list):
        """Reordena los filtros según una lista de nombres."""
        ordered = []
        for name in names:
            match = next((f for f in self.filters if f.name == name), None)
            if match:
                ordered.append(match)
        self.filters = ordered
        self._build_chain()

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
            results = [f.result() for f in concurrent.futures.as_completed(futures)]

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
