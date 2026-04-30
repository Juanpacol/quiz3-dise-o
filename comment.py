from dataclasses import dataclass, field


@dataclass
class Comment:
    text: str
    blocked: bool = False
    modified: bool = False
    flagged: bool = False
    reasons: list = field(default_factory=list)
