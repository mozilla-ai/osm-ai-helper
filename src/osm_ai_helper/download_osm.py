import json
from pathlib import Path
from typing import Dict, Optional

from fire import Fire
from loguru import logger

from osm_ai_helper.utils.osm import get_elements


@logger.catch(reraise=True)
def download_osm(
    area: str,
    output_dir: str,
    selector: str,
    discard: Optional[Dict[str, str]] = None,
):
    """Download OSM elements for the given areas and selector.

    Args:
        output_dir (str): Output directory.
        selector (str): OSM tag to select elements.
            Uses the [Overpass API](https://wiki.openstreetmap.org/wiki/Overpass_API/Language_Guide).

            Example: ["leisure=swimming_pool"](https://wiki.openstreetmap.org/wiki/Tag:leisure%3Dswimming_pool)

        area (str): Name of area to download.
            Can be city, state, country, etc.
            Uses the [Nominatim API](https://nominatim.org/release-docs/develop/api/Search/).

        discard (Optional[dict[str, str]], optional): Discard elements matching
            any of the given tags.
            Defaults to None.
            Example: {"location": "indoor", "building": "yes"}
    """
    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True, parents=True)

    discard = discard or {}

    logger.info(f"Downloading osm data for {area}")
    elements = [
        element
        for element in get_elements(selector, area=area)
        if all(element.get("tags", {}).get(k) != v for k, v in discard.items())
    ]

    output_file = output_path / f"{area}.json"
    logger.info(f"Writing {len(elements)} elements to {output_file}")
    output_file.write_text(json.dumps(elements))
    logger.success("Done!")


if __name__ == "__main__":
    Fire(download_osm)
