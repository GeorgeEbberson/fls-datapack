"""You should be able to break honeycomb blocks back to honeycomb with tools."""
from pathlib import Path
import shutil

OUTPUT_PATH = Path("minecraft", "loot_table", "blocks")  # Relative to `data`

LOOT_TABLE_FILE = Path(__file__).parent / "honeycomb_block_drop_honeycomb.json"


def generate_honeycomb_breaking(data_folder: Path):
    """Add create a folder and just copy the recipe in."""
    block_loot_table_folder = data_folder / OUTPUT_PATH
    block_loot_table_folder.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(LOOT_TABLE_FILE, block_loot_table_folder / "honeycomb_block.json")
