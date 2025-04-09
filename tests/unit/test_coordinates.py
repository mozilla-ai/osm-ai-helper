
from osm_ai_helper.utils.coordinates import (
  lat_lon_to_tile_col_row,
  pixel_col_row_to_meters_col_row,
  meters_col_row_to_lat_lon,
  TILE_SIZE
)

test_cases = [
    (-36.824380, 174.805511),
    (50.921286, 6.959694),
    (-16.504525, -68.154695),
    (37.352957, -121.926294),
    (0, 0)
]

for (lat, lon) in test_cases:
    for zoom in [18, 21]: # test multiple zoom levels; this should not make a difference
      x, y = lat_lon_to_tile_col_row(lat, lon, zoom)

      x_centre = (x * TILE_SIZE) + TILE_SIZE / 2
      y_center = (y * TILE_SIZE) + TILE_SIZE / 2
      x_metres, y_metres = pixel_col_row_to_meters_col_row(x_centre, y_center, zoom)

      (lat_center, lon_center) = meters_col_row_to_lat_lon(x_metres, y_metres)

      assert abs(lat - lat_center) < 0.001
      assert abs(lon - lon_center) < 0.001

print('coordinate tests passed')
