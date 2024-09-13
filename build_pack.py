"""Build the FLS datapack."""
from collections import OrderedDict
from pathlib import Path

from honeycomb_breaking import generate_honeycomb_breaking
from output_utils import ensure_empty_folder, write_dict_to_json, write_folder_to_zip
from universal_dyeing import generate_universal_dyeing

ROOT_FOLDER = Path(__file__).parent
OUTPUT_FOLDER = ROOT_FOLDER / "output"
DATA_FOLDER = OUTPUT_FOLDER / "data"

PACK_MCMETA_FILENAME = "pack.mcmeta"

DATAPACK_ZIP_PATH = OUTPUT_FOLDER / "fls-datapack.zip"

PACK_GEN_FUNCS = (generate_honeycomb_breaking, generate_universal_dyeing)

PACK_FORMAT = 48
PACK_DESCRIPTION = "FLS datapack"


def generate_pack_mcmeta(output_folder: Path):
    """Generate a pack.mcmeta file."""
    fmts = OrderedDict((
        ("min_inclusive", PACK_FORMAT),
        ("max_inclusive", PACK_FORMAT),
    ))

    pack = OrderedDict((
        ("pack_format", PACK_FORMAT),
        ("supported_formats", fmts),  # Ok since we upgrade so rarely
        ("description", PACK_DESCRIPTION),
    ))

    write_dict_to_json(
        output_folder / PACK_MCMETA_FILENAME,
        OrderedDict((("pack", pack),)),
    )


def main():
    """Construct the datapack then zip it."""
    ensure_empty_folder(OUTPUT_FOLDER)
    DATA_FOLDER.mkdir()

    for func in PACK_GEN_FUNCS:
        func(DATA_FOLDER)

    generate_pack_mcmeta(OUTPUT_FOLDER)
    write_folder_to_zip(OUTPUT_FOLDER, DATAPACK_ZIP_PATH)


if __name__ == "__main__":
    main()
