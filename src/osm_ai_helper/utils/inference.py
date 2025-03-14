from concurrent.futures import ThreadPoolExecutor
from typing import TYPE_CHECKING

import numpy as np
from loguru import logger
from shapely import Polygon, box

from osm_ai_helper.utils.coordinates import (
    TILE_SIZE,
    lat_lon_to_tile_col_row,
    lat_lon_to_pixel_col_row,
    pixel_col_row_to_meters_col_row,
    meters_col_row_to_lat_lon,
)
from osm_ai_helper.utils.osm import get_area
from osm_ai_helper.utils.tiles import download_tile

if TYPE_CHECKING:
    from sam2.sam2_image_predictor import SAM2ImagePredictor
    from ultralytics import YOLO


def split_area_into_lat_lon_centers(
    area_name: str, zoom: int, margin: int
) -> list[tuple[float, float]]:
    """
    Split the bounding box of `area_name` into a list of lat lon centers.

    If you iterate on the returned list using [run_inference][osm_ai_helper.run_inference.run_inference],
    you will cover the entire area.

    Args:
        area_name (str): Name of the area to split.
        zoom (int): value to be used in [run_inference][osm_ai_helper.run_inference.run_inference].
        margin (int): value to be used in [run_inference][osm_ai_helper.run_inference.run_inference].

    Returns:
        list[tuple[float, float]]: List of lat lon centers.
    """
    area = get_area(area_name)[0]
    south, north, west, east = area["boundingbox"]
    left, bottom = lat_lon_to_tile_col_row(float(south), float(west), zoom)
    right, top = lat_lon_to_tile_col_row(float(north), float(east), zoom)
    lat_lon_centers = []
    for col in range(left + margin, right + 1, (margin * 2) + 1):
        for row in range(top + margin, bottom + 1, (margin * 2) + 1):
            pixel_col_center = (col * 512) + 256
            pixel_row_center = (row * 512) + 256
            meters_col_center, meters_row_center = pixel_col_row_to_meters_col_row(
                pixel_col_center, pixel_row_center, zoom
            )
            lat_lon_center = meters_col_row_to_lat_lon(
                meters_col_center, meters_row_center
            )
            lat_lon_centers.append(lat_lon_center)
    return lat_lon_centers


def grouped_elements_to_mask(group, zoom, tile_col, tile_row):
    import cv2

    left_pixel = tile_col * TILE_SIZE
    top_pixel = tile_row * TILE_SIZE
    mask = np.zeros((TILE_SIZE, TILE_SIZE), dtype=np.uint8)
    bbox = box(left_pixel, top_pixel, left_pixel + TILE_SIZE, top_pixel + TILE_SIZE)
    for element in group:
        pixel_polygon = [
            lat_lon_to_pixel_col_row(point["lat"], point["lon"], zoom)
            for point in element["geometry"]
        ]
        bounded_polygon = Polygon(pixel_polygon).intersection(bbox).exterior.coords

        local_polygon = []
        for col, row in bounded_polygon:
            local_polygon.append((col - left_pixel, row - top_pixel))

        mask = cv2.fillPoly(
            mask, [np.array(local_polygon, dtype=np.int32)], color=(255, 0, 0)
        )
    return mask


def download_stacked_image_and_mask(
    bbox: tuple[float, float, float, float],
    grouped_elements: dict,
    zoom: int,
    mapbox_token: str,
) -> tuple[np.ndarray, np.ndarray]:
    """Download all tiles within a bounding box and stack them into a single image.

    All the grouped_elements are painted on the mask.

    Args:
        bbox (tuple): Bounding box in the form of (south, west, north, east).
        grouped_elements (dict): OpenStreetMap elements grouped with
            [group_elements_by_tile][osm_ai_helper.utils.tiles.group_elements_by_tile].
        zoom (int): Zoom level.
            See https://docs.mapbox.com/help/glossary/zoom-level/.
        mapbox_token (str): Mapbox token.
            See https://docs.mapbox.com/help/getting-started/access-tokens/.

    Returns:
        tuple: Stacked image and mask.
    """
    south, west, north, east = bbox
    left, top = lat_lon_to_tile_col_row(north, west, zoom)
    right, bottom = lat_lon_to_tile_col_row(south, east, zoom)

    stacked_image = np.zeros(
        ((right - left) * TILE_SIZE, (bottom - top) * TILE_SIZE, 3), dtype=np.uint8
    )
    stacked_mask = np.zeros(
        ((right - left) * TILE_SIZE, (bottom - top) * TILE_SIZE), dtype=np.uint8
    )

    with ThreadPoolExecutor() as executor:
        futures = {}
        for n_col, tile_col in enumerate(range(left, right)):
            for n_row, tile_row in enumerate(range(top, bottom)):
                group = grouped_elements[(tile_col, tile_row)]
                future = executor.submit(
                    download_tile, zoom, tile_col, tile_row, mapbox_token
                )
                futures[(n_row, n_col)] = future

        for n_col, tile_col in enumerate(range(left, right)):
            for n_row, tile_row in enumerate(range(top, bottom)):
                group = grouped_elements[(tile_col, tile_row)]

                img = futures[(n_row, n_col)].result()

                mask = grouped_elements_to_mask(group, zoom, tile_col, tile_row)

                stacked_image[
                    n_row * TILE_SIZE : (n_row + 1) * TILE_SIZE,
                    n_col * TILE_SIZE : (n_col + 1) * TILE_SIZE,
                ] = np.array(img)

                stacked_mask[
                    n_row * TILE_SIZE : (n_row + 1) * TILE_SIZE,
                    n_col * TILE_SIZE : (n_col + 1) * TILE_SIZE,
                ] = mask

    return stacked_image, stacked_mask


def yield_tile_corners(stacked_image: np.ndarray, tile_size: int, overlap: float):
    for top in range(0, stacked_image.shape[1], int(tile_size * (1 - overlap))):
        bottom = top + tile_size
        if bottom > stacked_image.shape[1]:
            bottom = stacked_image.shape[1]
            top = stacked_image.shape[1] - tile_size

        for left in range(0, stacked_image.shape[0], int(tile_size * (1 - overlap))):
            right = left + tile_size
            if right > stacked_image.shape[0]:
                right = stacked_image.shape[0]
                left = stacked_image.shape[0] - tile_size

            yield top, left, bottom, right


def predict_tile_batch(
    tile_batch,
    tile_coords_batch,
    bbox_predictor,
    sam_predictor,
    bbox_conf,
    bbox_pad,
    stacked_output,
):
    logger.debug(f"Predicting batch of {len(tile_batch)} tiles.")
    bbox_results_batch = bbox_predictor.predict(
        tile_batch, conf=bbox_conf, verbose=False
    )

    for tile_index, bbox_result in enumerate(bbox_results_batch):
        top, left, bottom, right = tile_coords_batch[tile_index]

        if len(bbox_result.boxes) == 0:
            continue

        sam_predictor.set_image(tile_batch[tile_index])

        for bbox in bbox_result:
            bbox_int = list(int(x) for x in bbox.boxes.xyxy[0])

            if bbox_pad > 0:
                bbox_int[0] = max(0, bbox_int[0] - bbox_pad)
                bbox_int[1] = max(0, bbox_int[1] - bbox_pad)
                bbox_int[2] = min(512, bbox_int[2] + bbox_pad)
                bbox_int[3] = min(512, bbox_int[3] + bbox_pad)

            masks, *_ = sam_predictor.predict(
                box=[bbox_int],
                multimask_output=False,
            )

            stacked_output[left:right, top:bottom] += masks[0].astype(np.uint8)

    return stacked_output


def tile_prediction(
    bbox_predictor: "YOLO",
    sam_predictor: "SAM2ImagePredictor",
    image: np.ndarray,
    overlap: float = 0.125,
    bbox_conf: float = 0.5,
    bbox_pad: int = 0,
    batch_size: int = 32,
) -> np.ndarray:
    """
    Predict on a large image by splitting it into tiles.

    Args:
        bbox_predictor (YOLO): YOLO bounding box.
            See https://docs.ultralytics.com/tasks/detect/.
        sam_predictor (SAM2ImagePredictor): Segment Anything Image Predictor.
            See https://github.com/facebookresearch/sam2?tab=readme-ov-file#image-prediction.
        image (np.ndarray): Image to predict on.
        overlap (float): Overlap between tiles.
            Defaults to 0.125.
        bbox_conf (float): Sets the minimum confidence threshold for detections.
            Defaults to 0.4.
        bbox_pad (int): Padding to be added to the predicted bbox.
            Defaults to 0.
        batch_size (int): Batch size for prediction.
            Defaults to 32.

    Returns:
        np.ndarray: Stacked output.
    """
    stacked_output = np.zeros((image.shape[0], image.shape[1]), dtype=np.uint8)
    tile_batch = []
    tile_coords_batch = []

    for top, left, bottom, right in yield_tile_corners(image, TILE_SIZE, overlap):
        logger.debug(f"Tile corners: {(top, left, bottom, right)}")
        tile_batch.append(image[left:right, top:bottom].copy())
        tile_coords_batch.append((top, left, bottom, right))

        if len(tile_batch) >= batch_size:
            stacked_output = predict_tile_batch(
                tile_batch,
                tile_coords_batch,
                bbox_predictor,
                sam_predictor,
                bbox_conf,
                bbox_pad,
                stacked_output,
            )
            tile_batch = []
            tile_coords_batch = []

    if tile_batch:
        stacked_output = predict_tile_batch(
            tile_batch,
            tile_coords_batch,
            bbox_predictor,
            sam_predictor,
            bbox_conf,
            bbox_pad,
            stacked_output,
        )

    return stacked_output
