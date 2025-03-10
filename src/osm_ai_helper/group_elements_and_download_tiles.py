import json
from concurrent.futures import as_completed
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from fire import Fire
from loguru import logger

from osm_ai_helper.utils.tiles import download_tile, group_elements_by_tile


@logger.catch(reraise=True)
def group_elements_and_download_tiles(
    elements_file: str, output_dir: str, mapbox_token: str, zoom: int = 18
):
    """
    Groups the elements by tile and downloads the satellite image corresponding to the tile.

    Args:
        elements_file (str): Path to the JSON file containing OSM elements.
            See [download_osm][osm_ai_helper.download_osm.download_osm].
        output_dir (str): Output directory.
            The images and annotations will be saved in this directory.
            The images will be saved as JPEG files and the annotations as JSON files.
            The names of the files will be in the format `{zoom}_{tile_col}_{tile_row}`.
        mapbox_token (str): [Mapbox](https://console.mapbox.com/) token.
        zoom (int, optional): Zoom level of the tiles to download.
            See https://docs.mapbox.com/help/glossary/zoom-level/.
            Defaults to 18.
    """
    annotation_path = Path(elements_file)
    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True, parents=True)

    elements = json.loads(annotation_path.read_text())

    logger.info("Grouping elements by tile")
    grouped = group_elements_by_tile(elements, zoom)

    download_tile_inputs = []
    annotation_names = []
    for (tile_col, tile_row), group in grouped.items():
        output_name = f"{zoom}_{tile_col}_{tile_row}"
        download_tile_inputs.append(
            (zoom, tile_col, tile_row, mapbox_token, f"{output_path / output_name}.jpg")
        )
        annotation_names.append(f"{output_path / output_name}.json")

    logger.info(f"Downloading tiles to {output_path}")
    with ThreadPoolExecutor() as executor:
        futures = [
            executor.submit(download_tile, *inputs) for inputs in download_tile_inputs
        ]
        for future in as_completed(futures):
            future.result()

    logger.info(f"Saving annotations to {output_path}")
    for annotation_name in annotation_names:
        Path(annotation_name).write_text(
            json.dumps(
                {
                    "elements": group,
                }
            )
        )


if __name__ == "__main__":
    Fire(group_elements_and_download_tiles)
