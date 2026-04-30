from comment import Comment
from filters import SpamFilter, ProfanityFilter, LengthFilter, LinkFilter, CapsFilter
from moderation_chain import ModerationChain
from config import FILTERS_ORDER, MAX_COMMENT_LENGTH


def print_result(comment: Comment):
    print(f"Texto:     {comment.text}")
    print(f"Bloqueado: {comment.blocked}")
    print(f"Modificado:{comment.modified}")
    print(f"Marcado:   {comment.flagged}")
    print(f"Razones:   {comment.reasons if comment.reasons else 'Ninguna'}")
    print("-" * 55)


def print_chain(chain: ModerationChain):
    nombres = [f.name for f in chain.filters]
    print(f"Cadena: {' -> '.join(nombres)}\n")


def main():
    FILTER_MAP = {
        "SpamFilter":     SpamFilter("FiltroSpam"),
        "ProfanityFilter": ProfanityFilter("FiltroPalabrasSoeces"),
        "LengthFilter":   LengthFilter("FiltroLongitud", max_length=MAX_COMMENT_LENGTH),
        "LinkFilter":     LinkFilter("FiltroEnlaces"),
        "CapsFilter":     CapsFilter("FiltroCaps"),
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

    print("\n=== CONFIGURACION DINAMICA ===\n")

    dynamic_chain = ModerationChain([
        SpamFilter("FiltroSpam"),
        ProfanityFilter("FiltroPalabrasSoeces"),
        LengthFilter("FiltroLongitud", max_length=MAX_COMMENT_LENGTH),
        LinkFilter("FiltroEnlaces"),
    ])

    test_comment = "IDIOTA mira https://spam.com oferta gratis"

    print("1) Cadena inicial:")
    print_chain(dynamic_chain)
    print_result(dynamic_chain.moderate(Comment(text=test_comment)))

    print("2) Despues de add_filter — FiltroCaps al inicio:")
    dynamic_chain.add_filter(CapsFilter("FiltroCaps"), position=0)
    print_chain(dynamic_chain)
    print_result(dynamic_chain.moderate(Comment(text=test_comment)))

    print("3) Despues de remove_filter — eliminar FiltroPalabrasSoeces:")
    dynamic_chain.remove_filter("FiltroPalabrasSoeces")
    print_chain(dynamic_chain)
    print_result(dynamic_chain.moderate(Comment(text=test_comment)))

    print("4) Despues de reorder — enlaces primero:")
    dynamic_chain.reorder(["FiltroEnlaces", "FiltroLongitud", "FiltroSpam", "FiltroCaps"])
    print_chain(dynamic_chain)
    print_result(dynamic_chain.moderate(Comment(text=test_comment)))


if __name__ == "__main__":
    main()