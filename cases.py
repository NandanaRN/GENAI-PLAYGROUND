"""
cases.py — Case library for Glitch in the Alibi v2

Each case is fully self-contained: victim, scene, suspects, the shared
false alibi, hard ground-truth facts, evidence items to discover, and
contradiction triggers used to drive the suspicion meter without any
extra API calls.
"""

CASE_LIBRARY = [
    {
        "id": "HARGROVE-114",
        "victim": "Walter Hargrove",
        "victim_detail": "a sharp-tongued publishing magnate, found face-down at his own desk",
        "scene": "a locked study in a townhouse on Eldridge Lane",
        "scene_short": "the study",
        "time_of_death": "between 9:00 PM and 9:30 PM",
        "method": "a single blow from a heavy bronze bookend",
        "suspects": ["Mara Voss", "Desmond Kray"],
        "suspect_roles": ["Hargrove's editorial director", "Hargrove's business partner"],
        "relationship": "business partners in Hargrove's publishing firm, both about to be cut out of a buyout deal",
        "shared_alibi": (
            "Both claim they were together in the kitchen downstairs, "
            "brewing coffee and going over quarterly numbers, and never "
            "went upstairs near the study."
        ),
        "alibi_location_short": "the kitchen",
        "hard_facts": [
            {
                "fact": "The kitchen radio was unplugged and silent all evening — it had been broken for a week.",
                "contradiction_triggers": ["radio was playing", "radio on", "music playing", "the radio", "song on the radio", "jazz on", "news on the radio"]
            },
            {
                "fact": "The coffee machine was never used that night; it was bone dry and cold to the touch the next morning.",
                "contradiction_triggers": ["smell of coffee", "coffee brewing", "fresh coffee", "pot of coffee", "coffee was hot", "brewed a pot"]
            },
            {
                "fact": "The kitchen window was jammed shut and painted over years ago — it does not open.",
                "contradiction_triggers": ["opened the window", "window was open", "breeze from the window", "cracked the window", "fresh air from outside"]
            },
            {
                "fact": "The single working light in the kitchen is a bare, harsh overhead bulb with no dimmer.",
                "contradiction_triggers": ["dimmed the lights", "soft lighting", "dim light", "mood lighting", "turned the lights down"]
            },
            {
                "fact": "The study door has a distinct, loud squeak that can be heard from the kitchen.",
                "contradiction_triggers": ["didn't hear anything", "quiet upstairs", "no sound from upstairs", "silent the whole time"]
            },
        ],
        "evidence": [
            {
                "id": "bent_bookend",
                "name": "Bent bronze bookend",
                "location": "the study",
                "reveal_text": "A bronze bookend shaped like an open book, one corner darkened and slightly bent out of shape, tucked behind a stack of manuscripts rather than left out in the open.",
                "relevance": "supports_guilty",
                "hint_question": "Ask a suspect directly whether they recognize the bronze bookend from the study.",
            },
            {
                "id": "torn_contract",
                "name": "Torn buyout contract page",
                "location": "the study",
                "reveal_text": "A single page from a buyout agreement, torn roughly in half, with handwritten margin notes in red ink: 'BOTH OUT BY Q3.'",
                "relevance": "supports_guilty",
                "hint_question": "Ask a suspect what they knew about the buyout deal and being pushed out.",
            },
            {
                "id": "muddy_footprint",
                "name": "Faint muddy footprint",
                "location": "the staircase",
                "reveal_text": "A single partial footprint on the third stair from the top, mostly dried, the kind left by someone climbing quickly rather than walking normally.",
                "relevance": "supports_guilty",
                "hint_question": "Ask a suspect if they went anywhere near the staircase that night.",
            },
            {
                "id": "untouched_mugs",
                "name": "Two clean coffee mugs",
                "location": "the kitchen",
                "reveal_text": "Two mugs sitting in the drying rack, bone dry, with a faint layer of dust on the rims — they have not been used or washed in at least a day.",
                "relevance": "supports_guilty",
                "hint_question": "Ask a suspect to describe exactly what they drank that night.",
            },
        ],
    },
    {
        "id": "DELACROIX-227",
        "victim": "Renee Delacroix",
        "victim_detail": "the celebrated head chef of Le Sillage, found among the wine racks",
        "scene": "the wine cellar beneath a restaurant called Le Sillage",
        "scene_short": "the wine cellar",
        "time_of_death": "around closing time, roughly 11:45 PM",
        "method": "a fall, possibly pushed, down the cellar's stone steps",
        "suspects": ["Theo Marchetti", "Adaeze Nwosu"],
        "suspect_roles": ["rival sous-chef", "head sommelier"],
        "relationship": "rival sous-chefs at the restaurant, both up for the head chef position Renee was about to announce",
        "shared_alibi": (
            "Both claim they were out back in the alley, sharing a smoke "
            "break and talking about the night's service, the entire time "
            "the kitchen was closing up."
        ),
        "alibi_location_short": "the back alley",
        "hard_facts": [
            {
                "fact": "It rained heavily from 11:15 PM to past midnight, and the alley flooded with two inches of standing water.",
                "contradiction_triggers": ["dry that night", "no rain", "clear sky", "weather was fine", "wasn't raining"]
            },
            {
                "fact": "The alley's motion-sensor light is broken and has been dark for over a month — total darkness back there at night.",
                "contradiction_triggers": ["light was on", "could see clearly", "alley light", "lit up", "saw each other clearly"]
            },
            {
                "fact": "The dumpster behind the kitchen was emptied that afternoon and was completely empty, not overflowing.",
                "contradiction_triggers": ["dumpster was full", "trash piled up", "smell from the dumpster", "overflowing"]
            },
            {
                "fact": "A delivery truck was blocking most of the alley from 11:00 PM until after midnight.",
                "contradiction_triggers": ["alley was empty", "nothing blocking", "clear path", "no truck"]
            },
            {
                "fact": "The back door alarm chirps loudly every time it opens, audible throughout the kitchen.",
                "contradiction_triggers": ["door didn't make a sound", "silent door", "no alarm", "snuck out quietly"]
            },
        ],
        "evidence": [
            {
                "id": "wet_apron",
                "name": "Damp chef's apron",
                "location": "the staff lockers",
                "reveal_text": "An apron hung up still slightly damp, though the kitchen towels nearby are bone dry — odd, for someone claiming they spent the whole break outside in dry weather.",
                "relevance": "supports_guilty",
                "hint_question": "Ask a suspect why their apron was still damp after their break.",
            },
            {
                "id": "broken_wine_glass",
                "name": "Shattered wine glass",
                "location": "the wine cellar",
                "reveal_text": "A wine glass shattered near the bottom of the cellar steps, stem snapped clean — the kind of break that happens when someone drops it suddenly, not from being knocked off a shelf.",
                "relevance": "supports_guilty",
                "hint_question": "Ask a suspect if they were in the wine cellar at all that night.",
            },
            {
                "id": "promotion_memo",
                "name": "Draft promotion memo",
                "location": "Renee's office",
                "reveal_text": "A printed draft memo announcing the new head chef, the name field left blank, dated for release the following morning.",
                "relevance": "supports_guilty",
                "hint_question": "Ask a suspect what they thought their chances were for the head chef promotion.",
            },
            {
                "id": "muddy_boots",
                "name": "Mud-caked kitchen clogs",
                "location": "the back hallway",
                "reveal_text": "A pair of kitchen clogs with fresh mud caked into the tread — unusual, since the alley out back was flooded with rainwater, not mud.",
                "relevance": "red_herring",
                "hint_question": "Ask a suspect about the mud on their shoes.",
            },
        ],
    },
    {
        "id": "ASHWORTH-309",
        "victim": "Gerald Ashworth",
        "victim_detail": "a reclusive lakeside property owner, found floating near his own dock",
        "scene": "the boathouse at the edge of Ashworth's lake property",
        "scene_short": "the boathouse",
        "time_of_death": "sometime between 7:30 PM and 8:15 PM",
        "method": "drowning, with a head wound suggesting he was struck first",
        "suspects": ["Priya Sandhu", "Felix Bauer"],
        "suspect_roles": ["Ashworth's stepdaughter", "Ashworth's stepson"],
        "relationship": "Ashworth's adult stepchildren, both named in a will that was about to be rewritten to exclude them entirely",
        "shared_alibi": (
            "Both claim they were up at the main house in the den, watching "
            "the same movie together on the projector the entire time."
        ),
        "alibi_location_short": "the den",
        "hard_facts": [
            {
                "fact": "The den's projector bulb burned out three days earlier and has not been replaced — it cannot project anything.",
                "contradiction_triggers": ["watching the movie", "on the screen", "projector was on", "watching the film", "movie was playing"]
            },
            {
                "fact": "There was a power flicker at 7:40 PM that reset every clock in the house, lasting about four seconds.",
                "contradiction_triggers": ["power never went out", "lights stayed on", "no flicker", "electricity was fine"]
            },
            {
                "fact": "The den's only couch is a small two-seater positioned facing the cold, unlit fireplace, not any screen.",
                "contradiction_triggers": ["sat on the big couch", "large sofa", "comfy couch facing the tv", "spread out on the couch"]
            },
            {
                "fact": "The household dog was locked in the den the entire evening and was barking loudly and persistently.",
                "contradiction_triggers": ["quiet evening", "no barking", "dog was calm", "dog wasn't there", "peaceful and quiet"]
            },
            {
                "fact": "The den windows look directly out over the dock and boathouse path.",
                "contradiction_triggers": ["couldn't see the dock", "no view of outside", "windows face the garden", "can't see the lake from there"]
            },
        ],
        "evidence": [
            {
                "id": "wet_sleeve",
                "name": "Damp jacket sleeve",
                "location": "the coat closet",
                "reveal_text": "A jacket hanging in the closet with one sleeve noticeably damp at the cuff, lake-water damp rather than rain damp.",
                "relevance": "supports_guilty",
                "hint_question": "Ask a suspect about the damp sleeve on their jacket.",
            },
            {
                "id": "will_draft",
                "name": "Unsigned will draft",
                "location": "Ashworth's study",
                "reveal_text": "A draft will on the desk, both stepchildren's names crossed out in pen, dated for a notary appointment scheduled for the next morning.",
                "relevance": "supports_guilty",
                "hint_question": "Ask a suspect what they knew about the new will.",
            },
            {
                "id": "dog_leash",
                "name": "Dog's leash, off the hook",
                "location": "near the front door",
                "reveal_text": "The dog's leash is missing from its usual hook by the door, suggesting someone took the dog out — which contradicts it being locked in the den all evening.",
                "relevance": "supports_guilty",
                "hint_question": "Ask a suspect whether they took the dog out at any point that evening.",
            },
            {
                "id": "broken_oar",
                "name": "Splintered oar",
                "location": "the boathouse",
                "reveal_text": "A wooden oar with a fresh splinter and a dark stain near the blade, leaning in the corner rather than stored on its usual rack.",
                "relevance": "supports_guilty",
                "hint_question": "Ask a suspect if they went into the boathouse that night.",
            },
        ],
    },
    {
        "id": "OKONKWO-441",
        "victim": "Simone Okonkwo",
        "victim_detail": "the gallery's senior curator, found in a storage room during her own opening reception",
        "scene": "a storage room behind the gallery's east wing",
        "scene_short": "the storage room",
        "time_of_death": "during the gallery's opening reception, around 8:50 PM",
        "method": "blunt force, likely from a fallen display pedestal",
        "suspects": ["Lucas Bennet", "Ines Romano"],
        "suspect_roles": ["junior curator", "gallery director"],
        "relationship": "gallery curators competing for the same promotion Simone was about to award that same night",
        "shared_alibi": (
            "Both claim they were together at the front reception desk the "
            "entire time, greeting guests and checking names off the list."
        ),
        "alibi_location_short": "the reception desk",
        "hard_facts": [
            {
                "fact": "The guest list that evening was entirely digital, displayed on a tablet with no paper backup at all.",
                "contradiction_triggers": ["paper list", "clipboard", "checked off the paper", "the printed list"]
            },
            {
                "fact": "A string quartet was playing live directly beside the reception desk the whole night, quite loudly.",
                "contradiction_triggers": ["quiet at the desk", "no music nearby", "peaceful at the front", "could hear each other clearly without trying"]
            },
            {
                "fact": "The reception desk has a clear, direct sightline straight down the east wing corridor.",
                "contradiction_triggers": ["couldn't see the east wing", "no view down the hall", "blocked view", "wall in the way"]
            },
            {
                "fact": "The east wing lights were intentionally dimmed to near-darkness for a lighting installation that evening.",
                "contradiction_triggers": ["east wing was bright", "well lit", "lights were on", "fully lit gallery"]
            },
            {
                "fact": "A spilled glass of red wine left a large, visible stain on the reception desk's white tablecloth around 8:30 PM.",
                "contradiction_triggers": ["clean tablecloth", "no spills", "spotless desk", "nothing spilled"]
            },
        ],
        "evidence": [
            {
                "id": "broken_pedestal",
                "name": "Cracked display pedestal",
                "location": "the storage room",
                "reveal_text": "A wooden display pedestal with a fresh crack along one edge, shoved against the wall rather than left where the body was found.",
                "relevance": "supports_guilty",
                "hint_question": "Ask a suspect if they were in the storage room at any point.",
            },
            {
                "id": "promotion_email",
                "name": "Printed promotion email",
                "location": "Simone's office",
                "reveal_text": "A printed email confirming the promotion announcement was scheduled for the end of the reception, with one name highlighted in yellow.",
                "relevance": "supports_guilty",
                "hint_question": "Ask a suspect what they expected to happen at the end of the reception.",
            },
            {
                "id": "scuffed_shoe",
                "name": "Scuff mark on dress shoe",
                "location": "the coat check",
                "reveal_text": "A pair of formal shoes with a fresh white scuff mark across the toe, consistent with the pale storage-room flooring rather than the gallery's dark hardwood.",
                "relevance": "supports_guilty",
                "hint_question": "Ask a suspect about the scuff on their shoes.",
            },
            {
                "id": "wine_stain_jacket",
                "name": "Wine-stained jacket cuff",
                "location": "the coat check",
                "reveal_text": "A jacket with a small red wine stain on the cuff, matching the stain at the reception desk — consistent with whoever spilled it, not necessarily suspicious on its own.",
                "relevance": "red_herring",
                "hint_question": "Ask a suspect about the wine stain on their sleeve.",
            },
        ],
    },
    {
        "id": "VANCE-558",
        "victim": "Oliver Vance",
        "victim_detail": "a tech startup founder, found in his office during his own company's launch party",
        "scene": "a glass-walled corner office on the building's top floor",
        "scene_short": "the office",
        "time_of_death": "during the launch party, around 9:15 PM",
        "method": "a fall from his office chair, head striking the corner of a glass desk",
        "suspects": ["Jordan Mbeki", "Tasha Lindqvist"],
        "suspect_roles": ["co-founder and CTO", "lead investor's representative"],
        "relationship": "co-founder and the representative of an investor pushing to remove Oliver as CEO that same week",
        "shared_alibi": (
            "Both claim they were together on the rooftop terrace the entire "
            "time, taking photos for the company's social media during the party."
        ),
        "alibi_location_short": "the rooftop terrace",
        "hard_facts": [
            {
                "fact": "It was extremely windy on the rooftop that night, strong enough that the party's outdoor decorations had to be taken down early.",
                "contradiction_triggers": ["calm up there", "no wind", "still air", "perfectly calm evening"]
            },
            {
                "fact": "The rooftop string lights short-circuited and went completely dark around 9:00 PM and stayed off the rest of the night.",
                "contradiction_triggers": ["lights were on", "well lit rooftop", "string lights glowing", "nicely lit photos"]
            },
            {
                "fact": "The rooftop bar ran out of ice around 8:45 PM and the bartender was loudly complaining about it to anyone nearby.",
                "contradiction_triggers": ["drinks with ice", "iced cocktail", "ice in the drinks", "plenty of ice"]
            },
            {
                "fact": "A small fire pit on the rooftop was lit and burning the entire evening, the only real light source once the string lights died.",
                "contradiction_triggers": ["no fire", "completely dark up there", "pitch black", "nothing burning"]
            },
            {
                "fact": "The elevator to the rooftop was out of service that night; the only way up was a narrow exterior fire escape stairwell.",
                "contradiction_triggers": ["took the elevator", "elevator up", "rode the elevator"]
            },
        ],
        "evidence": [
            {
                "id": "cracked_phone",
                "name": "Cracked phone screen",
                "location": "the office floor",
                "reveal_text": "A phone with a freshly cracked screen, half-hidden under the desk, the lock screen showing a missed call from Oliver's assistant at 9:12 PM.",
                "relevance": "supports_guilty",
                "hint_question": "Ask a suspect whether they were on a call with Oliver around 9:12 PM.",
            },
            {
                "id": "termination_draft",
                "name": "Draft termination letter",
                "location": "Oliver's desk drawer",
                "reveal_text": "A draft letter on Oliver's desk, dated that day, outlining plans to remove a board member 'effective immediately' — name field left blank but circled twice.",
                "relevance": "supports_guilty",
                "hint_question": "Ask a suspect if they knew Oliver was planning to remove someone from the board.",
            },
            {
                "id": "fire_escape_scuff",
                "name": "Scuffed fire escape door",
                "location": "the stairwell",
                "reveal_text": "Fresh scuff marks on the fire escape door at the rooftop level, paint scraped in a pattern consistent with someone pushing through it in a hurry.",
                "relevance": "supports_guilty",
                "hint_question": "Ask a suspect if they used the fire escape stairwell that night.",
            },
            {
                "id": "champagne_flute",
                "name": "Unfinished champagne flute",
                "location": "the office",
                "reveal_text": "A champagne flute on Oliver's desk, still cold, barely touched — odd for someone supposedly alone in his office working, not socializing.",
                "relevance": "red_herring",
                "hint_question": "Ask a suspect if they brought Oliver a drink that night.",
            },
        ],
    },
]
