"""
https://docs.mapbox.com/help/glossary/zoom-level/
https://github.com/geometalab/pyGeoTile
https://wiki.openstreetmap.org/wiki/Zoom_levels
https://wiki.openstreetmap.org/wiki/Slippy_map_tilenames#Python
"""

import math

EARTH_RADIUS = 6378137.0
TILE_SIZE = 512  # Mapbox uses 512x512 tiles
ORIGIN_SHIFT = 2.0 * math.pi * EARTH_RADIUS / 2.0
INITIAL_RESOLUTION = 2.0 * math.pi * EARTH_RADIUS / float(TILE_SIZE)


def resolution(zoom):
    return INITIAL_RESOLUTION / (2**zoom)


def lat_lon_to_meters_col_row(lat, lon):
    meter_col = lon * ORIGIN_SHIFT / 180.0
    meter_row = math.log(math.tan((90.0 + lat) * math.pi / 360.0)) / (math.pi / 180.0)
    meter_row = meter_row * ORIGIN_SHIFT / 180.0
    return meter_col, meter_row


def meters_col_row_to_pixel_col_row(meter_col, meter_row, zoom):
    pixel_col = (meter_col + ORIGIN_SHIFT) / resolution(zoom=zoom)
    pixel_row = (meter_row - ORIGIN_SHIFT) / resolution(zoom=zoom)
    return abs(round(pixel_col)), abs(round(pixel_row))


def pixel_col_row_to_meters_col_row(pixel_col, pixel_row, zoom):
    meter_col = pixel_col * resolution(zoom=zoom) - ORIGIN_SHIFT
    meter_row = pixel_row * resolution(zoom=zoom) - ORIGIN_SHIFT
    meter_col, meter_row = abs(meter_col), abs(meter_row)
    half_size = int((TILE_SIZE * 2**zoom) / 2)
    if pixel_col < half_size:
        meter_col *= -1
    if pixel_row > half_size:
        meter_row *= -1
    return meter_col, meter_row


def meters_col_row_to_lat_lon(meter_col, meter_row):
    lon = (meter_col / ORIGIN_SHIFT) * 180.0
    lat = (meter_row / ORIGIN_SHIFT) * 180.0
    lat = (
        180.0
        / math.pi
        * (2.0 * math.atan(math.exp(lat * math.pi / 180.0)) - math.pi / 2.0)
    )
    return lat, lon


def lat_lon_to_tile_col_row(lat, lon, zoom):
    lat_rad = math.radians(lat)
    n = 2.0**zoom
    tile_col = int((lon + 180.0) / 360.0 * n)
    tile_row = int((1.0 - math.asinh(math.tan(lat_rad)) / math.pi) / 2.0 * n)
    return (tile_col, tile_row)


def tile_col_row_to_lat_lon(tile_col, tile_row, zoom):
    n = 2.0**zoom
    lon_deg = tile_col / n * 360.0 - 180.0
    lat_rad = math.atan(math.sinh(math.pi * (1 - 2 * tile_row / n)))
    lat_deg = math.degrees(lat_rad)
    return (lat_deg, lon_deg)


def lat_lon_to_bbox(lat: float, lon: float, zoom: int, margin: int = 1):
    center_col, center_row = lat_lon_to_tile_col_row(lat, lon, zoom)
    left_col = center_col - margin
    top_row = center_row - margin
    right_col = center_col + margin
    bottom_row = center_row + margin

    north, west = tile_col_row_to_lat_lon(left_col, top_row, zoom)
    # `+ 1` to include the bottom right tiles.
    south, east = tile_col_row_to_lat_lon(right_col + 1, bottom_row + 1, zoom)
    return (south, west, north, east)


def lat_lon_to_pixel_col_row(lat, lon, zoom):
    return meters_col_row_to_pixel_col_row(*lat_lon_to_meters_col_row(lat, lon), zoom)
