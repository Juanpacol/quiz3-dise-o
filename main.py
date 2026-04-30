from comment import Comment
from filters import SpamFilter, ProfanityFilter, LengthFilter, LinkFilter, CapsFilter
from moderation_chain import ModerationChain
from config import FILTERS_ORDER, MAX_COMMENT_LENGTH


def print_result(comment: Comment):
    print(f"Texto:      {comment.text}")
    print(f"Bloqueado:  {comment.blocked}")
    print(f"Modificado: {comment.modified}")
    print(f"Marcado:    {comment.flagged}")
    print(f"Razones:    {comment.reasons if comment.reasons else 'Ninguna'}")
    print("-" * 55)


def print_chain(chain: ModerationChain):
    nombres = [f.name for f in chain.filters]
    print(f"Cadena actual: {' -> '.join(nombres)}\n")


def main():
    FILTER_MAP = {
        "SpamFilter": SpamFilter("FiltroSpam"),
        "ProfanityFilter": ProfanityFilter("FiltroPalabrasSoeces"),
        "LengthFilter": LengthFilter("FiltroLongitud", max_length=MAX_COMMENT_LENGTH),
        "LinkFilter": LinkFilter("FiltroEnlaces"),
    }
    filters = [FILTER_MAP[name] for name in FILTERS_ORDER]

    comments = [
        Comment(text="Este producto es genial, me encanto!"),
        Comment(text="Oferta especial, click aqui para ganar dinero gratis"),
        Comment(text="Eres un idiota y un inutil"),
        Comment(text="Mira este enlace: https://ejemplo.com para mas info"),
        Comment(text="Comentario muy largo: " + "a" * 200),
    ]

    print("=== MODERACION SECUENCIAL ===\n")
    chain = ModerationChain(filters)
    for comment in comments:
        print_result(chain.moderate(comment))

    print("\n=== MODERACION PARALELA ===\n")
    parallel_chain = ModerationChain(filters, parallel=True)
    parallel_comment = Comment(text="idiota mira https://spam.com oferta gratis")
    print_result(parallel_chain.moderate(parallel_comment))

    print("\n=== FILTROS CONFIGURABLES DINAMICAMENTE ===")
    print("Cada cadena es una configuracion distinta e inmutable.\n")

    print("1) Cadena original (4 filtros, orden config.py):")
    chain1 = ModerationChain([
        SpamFilter("FiltroSpam"),
        ProfanityFilter("FiltroPalabrasSoeces"),
        LengthFilter("FiltroLongitud", max_length=MAX_COMMENT_LENGTH),
        LinkFilter("FiltroEnlaces"),
    ])
    print_chain(chain1)
    print_result(chain1.moderate(Comment(text="HOLA mira https://spam.com oferta gratis")))

    print("2) Cadena con CapsFilter agregado al inicio:")
    chain2 = ModerationChain([
        CapsFilter("FiltroCaps"),
        SpamFilter("FiltroSpam"),
        ProfanityFilter("FiltroPalabrasSoeces"),
        LengthFilter("FiltroLongitud", max_length=MAX_COMMENT_LENGTH),
        LinkFilter("FiltroEnlaces"),
    ])
    print_chain(chain2)
    print_result(chain2.moderate(Comment(text="HOLA mira https://spam.com oferta gratis")))

    print("3) Cadena sin FiltroPalabrasSoeces:")
    chain3 = ModerationChain([
        CapsFilter("FiltroCaps"),
        SpamFilter("FiltroSpam"),
        LengthFilter("FiltroLongitud", max_length=MAX_COMMENT_LENGTH),
        LinkFilter("FiltroEnlaces"),
    ])
    print_chain(chain3)
    print_result(chain3.moderate(Comment(text="HOLA mira https://spam.com oferta gratis")))

    print("4) Cadena con orden reorganizado (enlaces primero):")
    chain4 = ModerationChain([
        LinkFilter("FiltroEnlaces"),
        LengthFilter("FiltroLongitud", max_length=MAX_COMMENT_LENGTH),
        SpamFilter("FiltroSpam"),
        CapsFilter("FiltroCaps"),
    ])
    print_chain(chain4)
    print_result(chain4.moderate(Comment(text="HOLA mira https://spam.com oferta gratis")))


if __name__ == "__main__":
    main()