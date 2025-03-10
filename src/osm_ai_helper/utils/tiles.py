from collections import defaultdict
from io import BytesIO
from typing import Dict, List

import numpy as np
import requests
from PIL import Image

from osm_ai_helper.utils.coordinates import TILE_SIZE, lat_lon_to_pixel_col_row

MAPBOX_TILES_API = "https://api.mapbox.com/styles/v1/mapbox/satellite-v9/tiles"


def group_elements_by_tile(elements: List[Dict], zoom: int) -> dict[tuple, list[dict]]:
    """Broup elements by the tiles they belong to, based on the zoom level.

    Each MAPBOX tile is a 512x512 pixel image.

    Args:
        elements (List[Dict]): List of elements from
            [download_osm][osm_ai_helper.download_osm.download_osm].
        zoom (int): Zoom level. See https://docs.mapbox.com/help/glossary/zoom-level/.

    Returns:
        dict[tuple, list[dict]]: Grouped elements.
    """
    grouped: dict[tuple, list[dict]] = defaultdict(list)

    for element in elements:
        pixel_polygon = []
        for point in element["geometry"]:
            pixel_point = lat_lon_to_pixel_col_row(point["lat"], point["lon"], zoom)
            pixel_polygon.append(pixel_point)

        pixel_polygon = np.array(pixel_polygon, dtype=np.int32)

        tiles = map(tuple, np.unique(pixel_polygon // TILE_SIZE, axis=0))
        for group in tiles:
            grouped[group].append(element)

    return grouped


def download_tile(
    zoom: int, tile_col: int, tile_row: int, token: str, output_file: str | None = None
) -> None | Image.Image:
    response = requests.get(
        f"{MAPBOX_TILES_API}/{zoom}/{tile_col}/{tile_row}?access_token={token}"
    )
    if output_file:
        with open(output_file, "wb") as f:
            f.write(response.content)
    else:
        return Image.open(BytesIO(response.content))
