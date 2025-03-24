import json
import xml.etree.ElementTree as ET


from osm_ai_helper.export_osm import export_osm, MAX_ELEMENTS_PER_OSMCHANGE


def test_export_osm(tmp_path):
    input_dir = tmp_path / "input"
    input_dir.mkdir(exist_ok=True, parents=True)

    output_dir = tmp_path / "output"

    (input_dir / "polygon1.json").write_text(
        json.dumps(
            [[1.0, 2.0], [3.0, 4.0], [5.0, 6.0], [1.0, 2.0]],
        )
    )
    (input_dir / "polygon2.json").write_text(
        json.dumps([[10.0, 20.0], [30.0, 40.0], [50.0, 60.0], [01.0, 20.0]])
    )
    export_osm(input_dir, output_dir)

    output_files = list(output_dir.iterdir())
    assert len(output_files) == 1
    osmchange = ET.fromstring(output_files[0].read_text())
    assert len(osmchange) == 3


def test_export_osm_multiple_files(tmp_path):
    input_dir = tmp_path / "input"
    input_dir.mkdir(exist_ok=True, parents=True)
    output_dir = tmp_path / "output"

    for i in range(MAX_ELEMENTS_PER_OSMCHANGE + 1):
        (input_dir / f"polygon{i}.json").write_text(
            json.dumps(
                [[1.0, 2.0], [3.0, 4.0], [5.0, 6.0], [1.0, 2.0]],
            )
        )

    export_osm(input_dir, output_dir)

    output_files = list(output_dir.iterdir())
    assert len(output_files) == 2
    osmchange = ET.fromstring(output_files[0].read_text())
    assert len(osmchange) == 3
