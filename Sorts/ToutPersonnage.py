from Effets.EffetInvoque import EffetInvoque
import Sort
def getSorts(lvl):
    """@summary: charge les sorts de début de combat
    @return: List <Sort>
    """
    # pylint: disable=unused-argument
    sorts = []
    sorts.append(Sort.Sort("Cawotte", 0, 4, 1, 6,
                               [EffetInvoque("Cawotte", False, cibles_possibles="",
                                             cible_non_requise=True)],
                               [], 0, 1, 1, 6, 0, "cercle", True,
                               description="Invoque une Cawotte"))
    return sorts