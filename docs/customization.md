# 🎨 **Customization Guide**

This OpenStreetMap AI Helper Blueprint is designed to be flexible and easily adaptable to your specific needs. This guide will walk you through some key areas you can customize to make the Blueprint your own.

---

## 🧠 **Changing the Model**

The default provided model is trained to detect swimming pools.

You can follow the [Create Dataset](https://colab.research.google.com/github/mozilla-ai/osm-ai-helper/blob/main/demo/create_dataset.ipynb) and [Finetune Model](https://colab.research.google.com/github/mozilla-ai/osm-ai-helper/blob/main/demo/finetune_model.ipynb).

When creating the dataset, you need to pick:

- A `selector` based on [OpenStreetMap tags](https://wiki.openstreetmap.org/wiki/Map_features).
    The example uses [`leisure=swimming_pool`](https://wiki.openstreetmap.org/wiki/Tag:leisure=swimming_pool).
    Try to pick elements that can be clearly delimited with a polygon and are easy to distinguish in the satellite images.
    A similar example would be a tenis court `leisure=pitch,sport=tennis`.

- An appropriate [`zoom` level](https://docs.mapbox.com/help/glossary/zoom-level/) (the example uses `18`).
    There is a tradeoff between easier detection (higher zoom levels) and covering a wider area on each tile (lower zoom levels).

## 🤝 **Contributing to the Blueprint**

Want to help improve or extend this Blueprint? Check out the **[Future Features & Contributions Guide](future-features-contributions.md)** to see how you can contribute your ideas, code, or feedback to make this Blueprint even better!
