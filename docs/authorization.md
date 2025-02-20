# Authorization

In order to use the OpenStreetMap AI Helper Blueprint, there are a couple of authorization
accounts you need to set up.

## `MAPBOX_TOKEN`

Used to download the satellite images when [creating a dataset](https://colab.research.google.com/github/mozilla-ai/osm-ai-helper/blob/main/demo/create_dataset.ipynb) and/or [running inference](https://colab.research.google.com/github/mozilla-ai/osm-ai-helper/blob/main/demo/run_inference.ipynb).

You need to:

- Create an account: https://console.mapbox.com/
- Follow this guide to obtain your [Default Public Token](https://docs.mapbox.com/help/getting-started/access-tokens/#your-default-public-token).

## `OSM_CLIENT_ID` and `OSM_CLIENT_SECRET`

Used to upload the results after [running inference](https://colab.research.google.com/github/mozilla-ai/osm-ai-helper/blob/main/demo/run_inference.ipynb) to the OpenStreetMap database.

You need to:

- Create an account: https://www.openstreetmap.org/user/new
- Register a new OAuth2 application: https://www.openstreetmap.org/oauth2/applications/new
    Grant `Modify the map (write_api)`.
    Set the redirect URL to `https://127.0.0.1:8000`.
- Copy and save the `Client ID` and `Client Secret`.

## `HF_TOKEN`

Only needed if you are [Creating a Dataset](https://colab.research.google.com/github/mozilla-ai/osm-ai-helper/blob/main/demo/create_dataset.ipynb) and/or [Finetuning a Model](https://colab.research.google.com/github/mozilla-ai/osm-ai-helper/blob/main/demo/finetune_model.ipynb) in order to upload the results to the [HuggingFace Hub](https://huggingface.co/docs/hub/index).

You need to:

- Create an account: https://huggingface.co/join
- Follow this guide about [`User Access Tokens`](https://huggingface.co/docs/hub/security-tokens)
