"""Generate a Minecraft data pack for recipes that allow universal dyeing."""
from collections import OrderedDict
import itertools
from pathlib import Path

from output_utils import Inline, write_dict_to_json

OUTPUT_PATH = Path("universal_dyeing", "recipe")  # Relative to `data`

# List of all the colours to generate items for.
COLOURS = (
    "black",
    "blue",
    "brown",
    "cyan",
    "gray",
    "green",
    "light_blue",
    "light_gray",
    "lime",
    "magenta",
    "orange",
    "pink",
    "purple",
    "red",
    "white",
    "yellow",
)

# Items whose dye should be a universal_dyeing tag rather than the item.
TAGGED_DYES = ("black", "blue", "brown", "white")

# Blocks to generate for, all will have 8 items + 1 dye for 8 items.
BLOCKS = (
    "candle",
    "concrete",
    "concrete_powder",
    "glazed_terracotta",
    "stained_glass",
    "stained_glass_pane",
    "terracotta",
    "wool",
)


def generate_universal_dyeing(data_folder: Path):
    """Do the generation."""

    recipe_folder = data_folder / OUTPUT_PATH
    recipe_folder.mkdir(parents=True, exist_ok=True)

    for block, colour in itertools.product(BLOCKS, COLOURS):

        # Quite why the VT maintainers didn't make a tag for every colour I have
        # no idea, they're clearly deranged.
        dye = (
            {"tag": f"universal_dyeing:dyes/{colour}_dye"}
            if colour in TAGGED_DYES else
            {"item": f"minecraft:{colour}_dye"}
        )

        key = OrderedDict((
            ("#", [Inline({"item": f"minecraft:{col}_{block}"}) for col in COLOURS]),
            ("O", Inline(dye)),
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
