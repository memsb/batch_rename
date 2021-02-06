import os
import time
from datetime import datetime
from shutil import copyfile
from string import Template


class BatchRename(Template):
    delimiter = '%'


def get_files(path):
    return [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]


def get_modification_time(file_path):
    timestamp = os.path.getmtime(file_path)
    return format_datetime(timestamp)


def get_creation_time(file_path):
    timestamp = os.stat(file_path).st_birthtime
    return format_datetime(timestamp)


def format_datetime(timestamp):
    date_time = datetime.fromtimestamp(timestamp)
    return date_time.replace(microsecond=0).isoformat()


def ensure_destination_exists(destination_path):
    if not os.path.isdir(destination_path):
        os.makedirs(destination_path)


def batch_rename(src_path, destination_path, format_string):
    ensure_destination_exists(destination_path)

    t = BatchRename(format_string)
    date = format_datetime(time.time())

    files = get_files(src_path)
    for i, filename in enumerate(files):
        base, ext = os.path.splitext(filename)
        file_path = os.path.join(src_path, filename)
        created_at = get_creation_time(file_path)
        modified_at = get_modification_time(file_path)

        new_name = t.substitute(c=created_at, m=modified_at, b=base, d=date, n=i, e=ext)
        new_path = os.path.join(destination_path, new_name)

        print('{0} --> {1}'.format(file_path, new_path))
        copyfile(file_path, new_path)


if __name__ == "__main__":
    input_folder = input('Source dir: ')
    output_folder = input('Destination dir: ')
    fmt = input(
        'Enter rename style (%c creation date %m modified date %d current date %b base name %n sequence %e-extension): '
    )
    batch_rename(input_folder, output_folder, fmt)
