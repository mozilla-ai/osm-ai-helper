<p align="center">
  <picture>
    <!-- When the user prefers dark mode, show the white logo -->
    <source media="(prefers-color-scheme: dark)" srcset="./images/Blueprint-logo-white.png">
    <!-- When the user prefers light mode, show the black logo -->
    <source media="(prefers-color-scheme: light)" srcset="./images/Blueprint-logo-black.png">
    <!-- Fallback: default to the black logo -->
    <img src="./images/Blueprint-logo-black.png" width="35%" alt="Project logo"/>
  </picture>
</p>

<div align="center">

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
[![Ultralytics](https://img.shields.io/badge/Ultralytics-008080?logo=ultralytics&logoColor=white)](https://ultralytics.com/)
[![SAM 2](https://img.shields.io/badge/SAM%202-0099FF?logo=meta&logoColor=white)](https://segment-anything.com/)
[![](https://dcbadge.limes.pink/api/server/YuMNeuKStr?style=flat)](https://discord.gg/YuMNeuKStr) <br>
[![Docs](https://github.com/mozilla-ai/osm-ai-helper/actions/workflows/docs.yaml/badge.svg)](https://github.com/mozilla-ai/osm-ai-helper/actions/workflows/docs.yaml/)
[![Tests](https://github.com/mozilla-ai/osm-ai-helper/actions/workflows/tests.yaml/badge.svg)](https://github.com/mozilla-ai/osm-ai-helper/actions/workflows/tests.yaml/)
[![Ruff](https://github.com/mozilla-ai/osm-ai-helper/actions/workflows/lint.yaml/badge.svg?label=Ruff)](https://github.com/mozilla-ai/osm-ai-helper/actions/workflows/lint.yaml/)

[Blueprints Hub](https://developer-hub.mozilla.ai/)
| [Documentation](https://mozilla-ai.github.io/osm-ai-helper/)
| [Getting Started](https://mozilla-ai.github.io/osm-ai-helper/getting-started)
| [Contributing](CONTRIBUTING.md)

</div>


# OSM-AI-helper: a Blueprint by Mozilla.ai for mapping Features in OpenStreetMap with Computer Vision
This Blueprint helps you use object detection and image segmentation models to identify and map features in OpenStreetMap.

<img src="./images/osm-ai-helper-diagram.png" width="800" alt="OSM-AI-helper Diagram" />

## Quick-start

Get started right away finding swimming pools and contributing them to OpenStreetMap:

| Google Colab | HuggingFace Spaces  | GitHub Codespaces |
| -------------| ------------------- | ----------------- |
| Process full Area <br>[![Inference Area](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/mozilla-ai/osm-ai-helper/blob/main/demo/run_inference_area.ipynb) <br> Around a Point <br> [![Inference point](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/mozilla-ai/osm-ai-helper/blob/main/demo/run_inference_point.ipynb) | [![Try on Spaces](https://img.shields.io/badge/%F0%9F%A4%97%20Try%20on-Spaces-blue)](https://huggingface.co/spaces/mozilla-ai/osm-ai-helper) | [![Try on Codespaces](https://github.com/codespaces/badge.svg)](https://github.com/codespaces/new?hide_repo_select=true&ref=main&repo=928839264&skip_quickstart=true&machine=standardLinux32gb) |

You can also create your own dataset and finetune a new model for a different use case:

| Create Dataset  | Finetune Model |
| --------------- | -------------- |
| [![Create Dataset](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/mozilla-ai/osm-ai-helper/blob/main/demo/create_dataset.ipynb) | [![Finetune Model](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/mozilla-ai/osm-ai-helper/blob/main/demo/finetune_model.ipynb) |


## License

This project is licensed under the AGPL-3.0 License. See the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! To get started, you can check out the [CONTRIBUTING.md](CONTRIBUTING.md) file.
