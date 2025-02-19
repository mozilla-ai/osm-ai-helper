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

# OSM-AI-helper: a Blueprint by Mozilla.ai for contributing to OpenStreetMap with the help of AI

[![](https://dcbadge.limes.pink/api/server/YuMNeuKStr?style=flat)](https://discord.gg/YuMNeuKStr)
[![Docs](https://github.com/mozilla-ai/osm-ai-helper/actions/workflows/docs.yaml/badge.svg)](https://github.com/mozilla-ai/osm-ai-helper/actions/workflows/docs.yaml/)
[![Tests](https://github.com/mozilla-ai/osm-ai-helper/actions/workflows/tests.yaml/badge.svg)](https://github.com/mozilla-ai/osm-ai-helper/actions/workflows/tests.yaml/)
[![Ruff](https://github.com/mozilla-ai/osm-ai-helper/actions/workflows/lint.yaml/badge.svg?label=Ruff)](https://github.com/mozilla-ai/osm-ai-helper/actions/workflows/lint.yaml/)

📘 To explore this project further and discover other Blueprints, visit the [**Blueprints Hub**](https://developer-hub.mozilla.ai/).

👉 📖 For more detailed guidance on using this project, please visit our [**Docs here**](https://mozilla-ai.github.io/osm-ai-helper/)

### Built with

- Python 3.10+
- [Ultralytics](https://github.com/ultralytics/ultralytics)
- [SAM 2](https://github.com/facebookresearch/sam2)


## Quick-start

Get started right away finding swimming pools and contributing them to OpenStreetMap:

| Find Swimming Pools |
| ------------------- |
| [![Run Inference](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/mozilla-ai/osm-ai-helper/blob/main/demo/run_inference.ipynb)

You can also create your own dataset and finetune a new model for a different use case:

| Create Dataset  | Finetune Model |
| --------------- | -------------- |
| [![Create Dataset](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/mozilla-ai/osm-ai-helper/blob/main/demo/create_dataset.ipynb) | [![Finetune Model](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/mozilla-ai/osm-ai-helper/blob/main/demo/finetune_model.ipynb) |


## License

This project is licensed under the Apache 2.0 License. See the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! To get started, you can check out the [CONTRIBUTING.md](CONTRIBUTING.md) file.
