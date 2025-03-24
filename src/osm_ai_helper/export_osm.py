import json
import xml.etree.ElementTree as ET
from pathlib import Path

from fire import Fire
from loguru import logger


MAX_ELEMENTS_PER_OSMCHANGE = 50


def convert_polygons(lon_lat_polygons: list[list[float]], tags: dict | None = None):
    osmchange = ET.Element(
        "osmChange",
        version="0.6",
        generator="https://github.com/mozilla-ai/osm-ai-helper",
    )
    create = ET.SubElement(osmchange, "create")

    n_nodes = 0
    n_ways = 0
    ways = []
    for lon_lat_polygon in lon_lat_polygons:
        n_ways += 1
        way = ET.Element("way", id=f"-{n_ways}", version="0")

        # Predicted polygons always contains a duplicate of the first point
        lon_lat_polygon.pop()

        first_node = n_nodes + 1
        for lon, lat in lon_lat_polygon:
            n_nodes += 1
            ET.SubElement(
                create,
                "node",
                id=f"-{n_nodes}",
                lon=f"{lon}",
                lat=f"{lat}",
                version="0",
            )
            ET.SubElement(way, "nd", ref=f"-{n_nodes}")

        # OSM requires to duplicate first point to close the polygon
        ET.SubElement(way, "nd", ref=f"-{first_node}")

        if tags:
            for k, v in tags.items():
                ET.SubElement(way, "tag", k=k, v=v)

        # ways need to be added as subelements only every node from every polygon has been added
        ways.append(way)

    for way in ways:
        create.append(way)

    ET.SubElement(osmchange, "modify")
    delete = ET.SubElement(osmchange, "delete")
    delete.set("if-unused", "true")
    return osmchange


@logger.catch(reraise=True)
def export_osm(results_dir: str, output_dir: str, tags: dict = None) -> None:
    """
    Export the polygons in `results_dir` to an [`.osc`](https://wiki.openstreetmap.org/wiki/OsmChange) file.

    Args:
        results_dir (str): Directory containing the results.
            The results should be in the format of `*.json` files.
            See [`run_inference`][osm_ai_helper.run_inference.run_inference].
    """
    output_dir = Path(output_dir)
    output_dir.mkdir(exist_ok=True, parents=True)

    lon_lat_polygons = [
        json.loads(result.read_text()) for result in Path(results_dir).glob("*.json")
    ]
    logger.info(f"Converting {len(lon_lat_polygons)} polygons to OsmChange format.")
    logger.info(
        f"Each set of {MAX_ELEMENTS_PER_OSMCHANGE} polygons will be saved to a separate file."
    )
    for n_polygon in range(0, len(lon_lat_polygons), MAX_ELEMENTS_PER_OSMCHANGE):
        to_be_converted = lon_lat_polygons[
            n_polygon : n_polygon + MAX_ELEMENTS_PER_OSMCHANGE
        ]
        osmchange = convert_polygons(to_be_converted, tags)
        output_file = f"{n_polygon}-{n_polygon + MAX_ELEMENTS_PER_OSMCHANGE}.osc"
        logger.info(f"Writing OsmChange to {output_file}")
        (output_dir / output_file).write_bytes(ET.tostring(osmchange, "utf-8"))


if __name__ == "__main__":
    Fire(export_osm)
