import json
from typing import Optional, Tuple

import requests


def get_area(area_name: str) -> dict:
    """Get the area from Nominatim.

    Uses the [Nominatim API](https://nominatim.org/release-docs/develop/api/Search/).

    Args:
        area_name (str): The name of the area.

    Returns:
        dict: The area found.
    """
    response = requests.get(
        f"https://nominatim.openstreetmap.org/search?q={area_name}&format=jsonv2",
        headers={"User-Agent": "Mozilla/5.0"},
    )
    response.raise_for_status()
    response_json = json.loads(response.content.decode())
    return response_json


def get_area_id(area_name: str) -> int:
    """
    Get the Nominatim ID of an area.

    Uses the [Nominatim API](https://nominatim.org/release-docs/develop/api/Search/).

    Args:
        area_name (str): The name of the area.

    Returns:
        int: The Nominatim ID of the area.
    """
    for area in get_area(area_name):
        osm_type = area.get("osm_type")
        osm_id = area.get("osm_id")
        if osm_type == "way":
            return osm_id + 2400000000
        if osm_type == "relation":
            return osm_id + 3600000000


def get_elements(
    selector: str,
    area: Optional[str] = None,
    bbox: Optional[Tuple[float, float, float, float]] = None,
) -> list[dict]:
    """
    Get elements from OpenStreetMap using the Overpass API.

    Uses the [Overpass API](https://wiki.openstreetmap.org/wiki/Overpass_API/Language_Guide).

    Args:
        selector (str): The selector to use.
            Example: "leisure=swimming_pool"
        area (Optional[str], optional): The area to search in.
            Can be city, state, country, etc.
            Defaults to None.

        bbox (Optional[Tuple[float, float, float, float]], optional): The bounding box to search in.
            Defaults to None.
            Format: https://wiki.openstreetmap.org/wiki/Overpass_API/Language_Guide#The_bounding_box

    Returns:
        The elements found.
    """
    query = "[out:json];"

    if area:
        area_id = get_area_id(area)
        query += f"area({area_id})->.searchArea;(way[{selector}](area.searchArea););"
    elif bbox:
        bbox_str = ",".join(map(str, bbox))
        query += f"(way[{selector}]({bbox_str}););"
    else:
        raise ValueError("area or bbox must be provided")

    query += " out body geom;"

    response = requests.get(
        "https://overpass-api.de/api/interpreter",
        params={"data": query},
        headers={"User-Agent": "Mozilla/5.0"},
    )
    response.raise_for_status()
    response_json = json.loads(response.content.decode())
    return response_json["elements"]
