import random
from enum import Enum

fifth_ed_bad_reactions = ["cringe.jpg", "mike.jpg", "nat1.gif", "nat1.jpg", "jazz.jpg"]
fifth_ed_good_reactions = ["heisenberg.gif", "joji.jpg", "mcmahon.gif", "nat20.jpg"]

sw_bad_reactions = ["bad1.gif", "bad2.gif", "bad3.gif", "bad4.gif",
                    "bad5.gif", "bad6.jpg", "bad7.jpg", "bad8.jpg", "bad9.gif", "bad10.gif"]
sw_good_reactions = ["good1.gif", "good2.gif", "good3.gif",
                     "good4.gif", "good5.gif", "good6.gif", "good7.gif", "good8.gif"]

class GameMode(Enum):
    WIZARDS_FIFTH_ED = 1
    STAR_WARS_FIFTH_ED = 2

def get_good_reaction (current_gamemode):
    path = "resources/reactions/5e/good/" + random.choice(fifth_ed_good_reactions)
    if current_gamemode == GameMode.STAR_WARS_FIFTH_ED:
       path = "resources/reactions/sw5e/good/" + random.choice(sw_good_reactions)
    return path

def get_bad_reaction(current_gamemode):
    path = "resources/reactions/5e/bad/" + random.choice(fifth_ed_bad_reactions)
    if current_gamemode == GameMode.STAR_WARS_FIFTH_ED:
        path = "resources/reactions/sw5e/bad/" + random.choice(sw_bad_reactions)
    return path
