# **Step-by-Step Guide: How the OpenStreetMap AI Helper Blueprint works**

Contributing to OpenStreetMap with the help of AI requires a model trained on an appropriate dataset.

We provide tools and example notebooks to:

- [Creating a custom dataset using ground truth data from OpenStreetMap](https://colab.research.google.com/github/mozilla-ai/osm-ai-helper/blob/main/demo/create_dataset.ipynb)
- [Finetuning a YOLO detector using the custom dataset](https://colab.research.google.com/github/mozilla-ai/osm-ai-helper/blob/main/demo/finetune_model.ipynb)

Once you have a trained model, you can [Run Inference](https://colab.research.google.com/github/mozilla-ai/osm-ai-helper/blob/main/demo/run_inference_point.ipynb) in order to find the type of elements you used to train the model (in the example, we chose swimming pools).

## **Overview**

The inference has 4 core stages:

## **Step 1: Pick a point in the map and download data around it**

![Lat Lon Point](./images/lat-lon-point.png)

After a point is selected, a bounding box is computed around it based on the `margin` argument.

All the existing elements of interest are downloaded from [OpenStreetMap](https://www.openstreetmap.org) using [`get_elements`](api.md/#osm_ai_helper.utils.osm.get_elements).

All the tiles are downloaded from [MapBox](https://www.mapbox.com/) and joined to create a `stacked image` using [`download_stacked_image_and_mask`](api.md/#osm_ai_helper.utils.inference.download_stacked_image_and_mask). The elements are grouped and converted to a `ground truth mask` for later usage.

![Stacked Image](./images/stacked-image.png)


## **Step 2: Run inference on the stacked image**

The stacked image is divided into tiles to run inference using [`tile_prediction`](api.md/#osm_ai_helper.utils.inference.tile_prediction).

For each tile, we run the trained [YOLO detector](https://docs.ultralytics.com/tasks/detect/).

If an object of interest is detected, we pass the bounding box to the provided [SAM2 model](https://github.com/facebookresearch/sam2) to obtain a segmentation mask.

![Input YOLO SAM2](./images/input-yolo-sam2.png)

All the predictions are aggregated into a single `stacked output mask`.

## **Step 3: Find existing, new and missed polygons**

All the individual mask blobs are converted to polygons for both the `stacked output mask` and the `ground truth mask`.

Based on overlap, all the polygons are categorized into `existing` (green), `new` (yellow) or `missed` (red).
The really relevant ones are the `new` (yellow), the others just serve as reference on how the model behaves
for polygons already existing in OpenStreetMap.

## **Step 4: Review, filter and upload the `new` polygons to OpenStreetMap**

The `new` polygons can be manually reviewed and filtered:

![Filter Polygons](./images/filter-polygons.png)

The ones you chose to `keep` will be uploaded to OpenStreetMap using [`upload_osm`](api.md/#osm_ai_helper.upload_osm.upload_osm).

!!! warning

    Once uploaded, the changes will be added to OpenStreetMap, so ensure you're confident about the ones you've kept.

![Polygon Uploaded](./images/polygon-uploaded.png)

## 🎨 **Customizing the Blueprint**

To better understand how you can tailor this Blueprint to suit your specific needs, please visit the **[Customization Guide](customization.md)**.

## 🤝 **Contributing to the Blueprint**

Want to help improve or extend this Blueprint? Check out the **[Future Features & Contributions Guide](future-features-contributions.md)** to see how you can contribute your ideas, code, or feedback to make this Blueprint even better!
