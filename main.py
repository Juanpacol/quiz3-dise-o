from comment import Comment
from filters import SpamFilter, ProfanityFilter, LengthFilter, LinkFilter
from moderation_chain import ModerationChain


def print_result(comment: Comment):
    print(f"Texto:      {comment.text}")
    print(f"Bloqueado:  {comment.blocked}")
    print(f"Modificado: {comment.modified}")
    print(f"Marcado:    {comment.flagged}")
    print(f"Razones:    {comment.reasons if comment.reasons else 'Ninguna'}")
    print("-" * 55)


def print_chain(chain: ModerationChain):
    nombres = [f.name for f in chain.filters]
    print(f"Cadena actual: {' → '.join(nombres)}\n")


def main():
    filters = [
        SpamFilter("FiltroSpam"),
        ProfanityFilter("FiltroPalabrasSoeces"),
        LengthFilter("FiltroLongitud", max_length=100),
        LinkFilter("FiltroEnlaces"),
    ]

    # --- Cadena original ---
    print("=== CADENA ORIGINAL ===")
    chain = ModerationChain(filters)
    print_chain(chain)
    print_result(chain.moderate(Comment(text="Oferta especial, click aqui para ganar dinero gratis")))

    # --- Agregar un filtro dinámicamente ---
    print("=== DESPUÉS DE AGREGAR FiltroExtra AL INICIO ===")
    chain.add_filter(SpamFilter("FiltroExtra"), position=0)
    print_chain(chain)

    # --- Eliminar un filtro dinámicamente ---
    print("=== DESPUÉS DE ELIMINAR FiltroPalabrasSoeces ===")
    chain.remove_filter("FiltroPalabrasSoeces")
    print_chain(chain)
    print_result(chain.moderate(Comment(text="Eres un idiota y un inutil")))

    # --- Reordenar dinámicamente ---
    print("=== DESPUÉS DE REORDENAR ===")
    chain.reorder(["FiltroEnlaces", "FiltroLongitud", "FiltroSpam", "FiltroExtra"])
    print_chain(chain)
    print_result(chain.moderate(Comment(text="Mira este enlace: https://ejemplo.com oferta gratis")))

    # --- Modo paralelo ---
    print("=== MODERACIÓN PARALELA ===\n")
    parallel_chain = ModerationChain(filters, parallel=True)
    print_result(parallel_chain.moderate(Comment(text="idiota mira https://spam.com oferta gratis")))


if __name__ == "__main__":
    main()
