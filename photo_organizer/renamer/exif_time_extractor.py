import datetime
import logging
from pathlib import Path
from typing import Optional

from photo_organizer.exif.exif_tool import ExifTool


class MetadataTimeExtractor:
    """
    The time extractor from EXIF data
    """

    def __init__(self, working_dir: Path):
        self.exif_tool = ExifTool(working_dir / "exiftool.exe")
        self.exif_date_field_to_format = {
            "EXIF:DateTimeOriginal": "%Y:%m:%d %H:%M:%S",   # Prefer EXIF:DateTimeOriginal for non .mov files
            "QuickTime:CreationDate": "%Y:%m:%d %H:%M:%S%z",  # Prefer CreationDate since it has timezone info
            "QuickTime:MediaCreateDate": "%Y:%m:%d %H:%M:%S"  # Fall back to MediaCreateDate
        }

        self.exif_date_backup_fields_to_format = {
            "File:FileModifyDate": "%Y:%m:%d %H:%M:%S%z"
        }

    def get_time(self, path: Path) -> Optional[datetime.datetime]:
        metadata = self.exif_tool.get_metadata(path)[0]
        logging.debug(f"{path}: {metadata}")

        for exif_date_field, date_format in self.exif_date_field_to_format.items():
            if exif_date_field not in metadata:
                continue
            try:
                return datetime.datetime.strptime(metadata[exif_date_field], date_format)
            except ValueError:
                return None

        for exif_date_field, date_format in self.exif_date_backup_fields_to_format.items():
            if exif_date_field in metadata:
                logging.warning(f"Unreliable date {exif_date_field} used for {path} = {metadata[exif_date_field]}")
                return datetime.datetime.strptime(metadata[exif_date_field], date_format)

        return None
