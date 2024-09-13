"""Helpers for writing better (nicer) JSON."""
import hashlib
import json
from pathlib import Path
import shutil
import uuid
import zipfile


class Inline:
    def __init__(self, value):
        self.value = value


class InlineEncoder(json.JSONEncoder):
    """Keep an object inline rather than exploding to multiple lines.

    Stolen from https://stackoverflow.com/questions/13249415/
    how-to-implement-custom-indentation-when-pretty-printing-with-the-json-module
    (see Erik Kaplun's answer).
    """

    def __init__(self, *args, **kwargs):
        super(InlineEncoder, self).__init__(*args, **kwargs)
        self.kwargs = dict(kwargs)
        del self.kwargs['indent']
        self._replacement_map = {}

    def default(self, o):
        if isinstance(o, Inline):
            key = uuid.uuid4().hex
            self._replacement_map[key] = json.dumps(o.value, **self.kwargs)
            return "@@%s@@" % (key,)
        else:
            return super(InlineEncoder, self).default(o)

    def encode(self, o):
        result = super(InlineEncoder, self).encode(o)
        for k, v in iter(self._replacement_map.items()):
            result = result.replace('"@@%s@@"' % (k,), v)
        return result


def ensure_empty_folder(folder: Path):
    """Make sure `folder` exists and is empty."""
    if folder.exists():
        shutil.rmtree(folder)
    folder.mkdir()


def compute_zip_md5(file_path: Path):
    """Compute the MD5 hash of the contents of a .zip."""
    archive = zipfile.ZipFile(file_path, "r")
    zip_md5 = hashlib.md5()
    for file_name in archive.namelist():
        zip_md5.update(archive.read(file_name))
    return zip_md5.hexdigest()


def add_hash_to_filename(zip_path: Path):
    """Compute an MD5 hash and add it to the end of `zip_path`."""
    hash_to_add = compute_zip_md5(zip_path)[:8]
    zip_path.rename(zip_path.parent / (zip_path.stem + "-" + hash_to_add + zip_path.suffix))


def write_folder_to_zip(folder: Path, zip_path: Path):
    """Write each file of `folder` to `zip_name`."""
    files = [x.relative_to(folder) for x in folder.rglob("*")]
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as archive:
        for file in files:
            archive.write(folder / file, file)
    add_hash_to_filename(zip_path)


def write_dict_to_json(filename: Path, data_dict: dict):
    """Dump `data_dict` to a JSON file called `filename`."""
    with open(filename, "a+") as f:
        f.write(json.dumps(data_dict, indent=4, cls=InlineEncoder))
