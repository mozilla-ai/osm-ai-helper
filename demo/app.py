import os
from pathlib import Path
from shutil import move

import folium
import streamlit as st
from branca.element import MacroElement
from jinja2 import Template
from huggingface_hub import hf_hub_download
from PIL import Image
from streamlit_folium import st_folium

from osm_ai_helper.run_inference import run_inference
from osm_ai_helper.upload_osm import upload_osm


@st.fragment
def show_map():
    class LatLngPopup(MacroElement):
        _template = Template(
            """
                {% macro script(this, kwargs) %}
                    var {{this.get_name()}} = L.popup();
                    function latLngPop(e) {
                        {{this.get_name()}}
                            .setLatLng(e.latlng)
                            .setContent(e.latlng.lat.toFixed(4) + ", " + e.latlng.lng.toFixed(4))
                            .openOn({{this._parent.get_name()}});
                        }
                    {{this._parent.get_name()}}.on('click', latLngPop);
                {% endmacro %}
                """
        )

        def __init__(self):
            super().__init__()
            self._name = "LatLngPopup"

    m = folium.Map(location=[42.8075, -8.1519], zoom_start=8, tiles="OpenStreetMap")
    m.add_child(LatLngPopup())

    st_folium(m, height=400, width=800)


@st.fragment
def inference(lat_lon):
    with st.spinner("Downloading model..."):
        hf_hub_download(
            "mozilla-ai/swimming-pool-detector",
            filename="model.pt",
            repo_type="model",
            local_dir="models",
        )
    with st.spinner("Downloading image and Running inference..."):
        output_path, existing, new, missed = run_inference(
            yolo_model_file="models/model.pt",
            output_dir="/tmp/results",
            lat_lon=lat_lon,
            margin=2,
            save_full_images=False,
            batch_size=64,
        )
    return output_path, existing, new


@st.fragment
def handle_polygon(polygon):
    raw_image = Image.open(polygon.with_suffix(".png"))
    painted_image = Image.open(f"{polygon.parent}/{polygon.stem}_painted.png")

    st.subheader(f"Reviewing: {polygon.name}")

    col1, col2 = st.columns(2)

    with col1:
        st.image(raw_image, caption="Raw Image", use_container_width=True)
    with col2:
        st.image(painted_image, caption="Painted Image", use_container_width=True)

    if st.button("Keep Polygon", key=f"keep_{polygon}"):
        keep_folder = polygon.parent / "keep"
        keep_folder.mkdir(parents=True, exist_ok=True)
        move(polygon, keep_folder / polygon.name)
        st.success(f"Polygon moved to {keep_folder}")
    elif st.button("Discard Polygon", key=f"discard_{polygon.stem}"):
        discard_folder = polygon.parent / "discard"
        discard_folder.mkdir(parents=True, exist_ok=True)
        move(polygon, discard_folder / polygon.name)
        st.warning(f"Polygon moved to {discard_folder}")


@st.fragment
def upload_results(output_path):
    st.divider()
    st.header("Upload all polygons in `keep`")

    st.markdown(
        "The results will be uploaded using the [osm-ai-helper](https://www.openstreetmap.org/user/osm-ai-helper) profile."
    )
    st.markdown(
        "You can check the [Colab Notebook](ttps://colab.research.google.com/github/mozilla-ai/osm-ai-helper/blob/main/demo/run_inference_point.ipynb)"
        " and the [Authorization Guide](https://mozilla-ai.github.io/osm-ai-helper/authorization)"
        " to contribute with your own OpenStreetMap account."
    )
    contributor = st.text_input("(Optional) Indicate your name for attribution")
    if st.button("Upload all polygons in `keep`"):
        if contributor:
            comment = f"Add Swimming Pools. Contributed by {contributor}"
        else:
            comment = "Add Swimming Pools"

        changeset = upload_osm(
            results_dir=output_path / "keep",
            client_id=os.environ["OSM_CLIENT_ID"],
            client_secret=os.environ["OSM_CLIENT_SECRET"],
            comment=comment,
        )
        st.success(
            f"Changeset created: https://www.openstreetmap.org/changeset/{changeset}"
        )


st.title("OpenStreetMap AI Helper")

st.markdown(
    """
This demo was created with the repo [mozilla-ai/osm-ai-helper](https://github.com/mozilla-ai/osm-ai-helper).

It uses the model [mozilla-ai/swimming-pool-detector](https://huggingface.co/mozilla-ai/swimming-pool-detector).

You can check the [Create Dataset](https://colab.research.google.com/github/mozilla-ai//osm-ai-helper/blob/main/demo/create_dataset.ipyn)
and [Finetune Model](https://colab.research.google.com/github/mozilla-ai//osm-ai-helper/blob/main/demo/finetune_model.ipynb) notebooks to learn how to train your own model.
"""
)

st.divider()

st.subheader("Click on the map to select a latitude and longitude.")

st.markdown(
    """
The model will try to find swimming pools around this location.

Note that this model was trained with data from [Galicia](https://nominatim.openstreetmap.org/ui/details.html?osmtype=R&osmid=349036&class=boundary),
so it might fail to generalize to significantly different places.
"""
)

show_map()

lat_lon = st.text_input("Paste the copied (latitude, longitude)")

if st.button("Run Inference") and lat_lon:
    lat, lon = lat_lon.split(",")
    output_path, existing, new = inference(
        lat_lon=(float(lat.strip()), float(lon.strip()))
    )

    st.info(f"Found {len(existing)} swimming pools already in OpenStreetMaps.")

    if new:
        st.divider()
        st.header("Review `new` swimming pools")
        st.markdown(
            "Every `new` swimming pool will be displayed at the center of the image in `yellow`."
        )
        st.markdown(
            "Swimming pools in other colors are those already existing in OpenStreetMap and they just "
            "indicate whether the model has found them (`green`) or missed them (`red`)."
        )
        for new in Path(output_path).glob("*.json"):
            handle_polygon(new)

        upload_results(output_path)
    else:
        st.warning("No `new` swimming pools were found. Try a different location.")
