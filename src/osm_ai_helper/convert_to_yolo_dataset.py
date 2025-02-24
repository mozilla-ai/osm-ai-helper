import json
from pathlib import Path
from typing import Dict, List

from fire import Fire
from loguru import logger
from shapely.geometry import box, Polygon

from osm_ai_helper.utils.coordinates import (
    TILE_SIZE,
    lat_lon_to_meters_col_row,
    meters_col_row_to_pixel_col_row,
)


def grouped_elements_to_annotation(
    group: List[Dict], zoom: int, tile_col: int, tile_row: int
) -> str:
    """
    Output format: https://docs.ultralytics.com/datasets/detect/
    """
    annotation = ""
    left_pixel = tile_col * TILE_SIZE
    top_pixel = tile_row * TILE_SIZE
    bbox = box(left_pixel, top_pixel, left_pixel + TILE_SIZE, top_pixel + TILE_SIZE)
    for element in group:
        pixel_polygon = [
            meters_col_row_to_pixel_col_row(
                *lat_lon_to_meters_col_row(point["lat"], point["lon"]), zoom
            )
            for point in element["geometry"]
        ]
        try:
            bounded_polygon = Polygon(pixel_polygon).intersection(bbox)
        except AttributeError:
            continue
        min_col, min_row, max_col, max_row = bounded_polygon.bounds
        col_center = (min_col + max_col) / 2
        col_center = (col_center - left_pixel) / TILE_SIZE
        col_center = round(col_center, 2)
        row_center = (min_row + max_row) / 2
        row_center = (row_center - top_pixel) / TILE_SIZE
        row_center = round(row_center, 2)
        width = max_col - min_col
        width /= TILE_SIZE
        width = round(width, 2)
        height = max_row - min_row
        height /= TILE_SIZE
        height = round(height, 2)
        annotation += f"0 {col_center} {row_center} {width} {height}\n"

    return annotation


@logger.catch(reraise=True)
def convert_to_yolo_dataset(
    input_dir: str,
):
    """Convert the output of `group_elements_and_download_tiles.py` to the [YOLO format](https://docs.ultralytics.com/datasets/detect/).

    Args:
        input_dir (str): Input directory containing the images and annotations.
            The images are expected to be in the format `zoom_tile_col_tile_row.jpg`.
            The annotations are expected to be in the format `zoom_tile_col_tile_row.json`.
    """
    input_path = Path(input_dir)

    for image_path in input_path.glob("**/*.jpg"):
        annotation_path = image_path.with_suffix(".json")
        annotation = json.loads(annotation_path.read_text())
        zoom, tile_col, tile_row = map(int, image_path.stem.split("_"))

        yolo_annotation = grouped_elements_to_annotation(
            annotation["elements"], zoom, tile_col, tile_row
        )
        image_path.with_suffix(".txt").write_text(yolo_annotation)


if __name__ == "__main__":
    Fire(convert_to_yolo_dataset)
