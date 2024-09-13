"""Generate a Minecraft data pack for recipes that allow universal dyeing."""
from collections import OrderedDict
import itertools
from pathlib import Path

from output_utils import Inline, write_dict_to_json

# All relative to `data`
BASE_PATH = Path("universal_dyeing")
RECIPE_PATH = BASE_PATH / "recipe"
TAGS_PATH = BASE_PATH / "tags" / "item"
ADVANCEMENT_PATH = BASE_PATH / "advancement" / "recipes" / "building_blocks" / "universal_dyeing"

# All the colours, and any "extra" dyes (on top of <colour>_dye)
EXTRA_DYES = {
    "black": ("ink_sac",),
    "blue": ("lapis_lazuli",),
    "brown": ("cocoa_beans",),
    "cyan": None,
    "gray": None,
    "green": None,
    "light_blue": None,
    "light_gray": None,
    "lime": None,
    "magenta": None,
    "orange": None,
    "pink": None,
    "purple": None,
    "red": None,
    "white": ("bone_meal",),
    "yellow": None,
}
COLOURS = EXTRA_DYES.keys()

# Blocks to generate for, all will have 8 items + 1 dye for 8 items.
ITEMS = (
    "candle",
    "concrete",
    "concrete_powder",
    "glazed_terracotta",
    "stained_glass",
    "stained_glass_pane",
    "terracotta",
    "wool",
)


def generate_recipes(data_folder: Path):
    """Generate all the recipes."""
    recipe_folder = data_folder / RECIPE_PATH
    recipe_folder.mkdir(parents=True, exist_ok=True)

    for block, colour in itertools.product(ITEMS, COLOURS):
        key = OrderedDict((
            ("#", [Inline({"item": f"minecraft:{col}_{block}"}) for col in COLOURS]),
            ("O", Inline({"tag": f"universal_dyeing:dyes/{colour}_dye"})),
        ))

        result = OrderedDict((
            ("id", f"minecraft:{colour}_{block}"),
            ("count", 8)
        ))

        recipe = OrderedDict((
            ("type", "crafting_shaped"),
            ("pattern", ["###", "#O#", "###"]),
            ("key", key),
            ("result", result),
            ("group", f"universal_dyeing_{block}"),
        ))

        output_file = recipe_folder / f"{colour}_{block}.json"
        write_dict_to_json(output_file, recipe)


def generate_tags(data_folder: Path):
    """Generate a tag for each colour dye."""
    tags_folder = data_folder / TAGS_PATH
    tags_folder.mkdir(parents=True, exist_ok=True)

    dyes_folder = tags_folder / "dyes"
    dyes_folder.mkdir(parents=True, exist_ok=True)

    for colour in COLOURS:
        dyes = (f"{colour}_dye",) + (EXTRA_DYES[colour] if EXTRA_DYES[colour] else tuple())
        tag = OrderedDict((("values", [f"minecraft:{item}" for item in dyes]),))
        write_dict_to_json(dyes_folder / f"{colour}_dye.json", Inline(tag))

    for item in ITEMS:
        items = [f"minecraft:{colour}_{item}" for colour in COLOURS]
        tag = OrderedDict((("values", items),))
        write_dict_to_json(tags_folder / f"{item}.json", tag)

    named_dyes = [f"{colour}_dye" for colour in COLOURS]
    other_dyes = sum([list(x) for x in EXTRA_DYES.values() if x], [])
    all_dyes = named_dyes + other_dyes
    tag = OrderedDict((("values", [f"minecraft:{item}" for item in all_dyes]),))
    write_dict_to_json(tags_folder / "dyes.json", tag)


def generate_advancements(data_folder: Path):
    """Generate advancements that "award" the recipes to the players."""
    advancement_folder = data_folder / ADVANCEMENT_PATH
    advancement_folder.mkdir(parents=True, exist_ok=True)

    has_dye = OrderedDict((
        ("trigger", "minecraft:inventory_changed"),
        ("conditions", Inline({"items": [{"items": "#universal_dyeing:dyes"}]}))
    ))

    for item in ITEMS:
        has_block = OrderedDict((
            ("trigger", "minecraft:inventory_changed"),
            ("conditions", Inline({"items": [{"items": f"#minecraft:{item}"}]}))
        ))

        criteria = OrderedDict((
            ("has_block", has_block),
            ("has_dye", has_dye),
        ))

        root = OrderedDict((
            ("parent", "minecraft:recipes/root"),
            ("criteria", criteria),
            ("requirements", Inline([["has_block"], ["has_dye"]])),
            ("rewards", {"recipes": [f"universal_dyeing:{colour}_{item}" for colour in COLOURS]}),
        ))
        write_dict_to_json(advancement_folder / f"{item}.json", root)


def generate_universal_dyeing(data_folder: Path):
    """Do the generation."""
    generate_recipes(data_folder)
    generate_tags(data_folder)
    generate_advancements(data_folder)
