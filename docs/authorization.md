# Authorization

In order to use the OpenStreetMap AI Helper Blueprint, there are a couple of authorization
accounts you need to set up.

## `MAPBOX_TOKEN`

Used to download the satellite images when [creating a dataset](https://colab.research.google.com/github/mozilla-ai/osm-ai-helper/blob/main/demo/create_dataset.ipynb) and/or [running inference](https://colab.research.google.com/github/mozilla-ai/osm-ai-helper/blob/main/demo/run_inference_point.ipynb).

You need to:

- Create an account: https://console.mapbox.com/
- Follow this guide to obtain your [Default Public Token](https://docs.mapbox.com/help/getting-started/access-tokens/#your-default-public-token).

## `HF_TOKEN`

Only needed if you are [Creating a Dataset](https://colab.research.google.com/github/mozilla-ai/osm-ai-helper/blob/main/demo/create_dataset.ipynb) and/or [Finetuning a Model](https://colab.research.google.com/github/mozilla-ai/osm-ai-helper/blob/main/demo/finetune_model.ipynb) in order to upload the results to the [HuggingFace Hub](https://huggingface.co/docs/hub/index).

You need to:

- Create an account: https://huggingface.co/join
- Follow this guide about [`User Access Tokens`](https://huggingface.co/docs/hub/security-tokens)
