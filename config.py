SPAM_WORDS = [
    "oferta",
    "gratis",
    "click aqui",
    "gana dinero"
]

PROFANITY_WORDS = [
    "estupido",
    "idiota",
    "inutil"
]

MAX_COMMENT_LENGTH = 100

FILTERS_ORDER = [
    "SpamFilter",
    "ProfanityFilter",
    "LengthFilter",
    "LinkFilter"
]

ENABLE_PARALLEL_MODE = False
