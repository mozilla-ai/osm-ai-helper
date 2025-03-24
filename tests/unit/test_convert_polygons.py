import xml.etree.ElementTree as ET


from osm_ai_helper.export_osm import convert_polygons


def test_convert_polygons_empty_polygons():
    lon_lat_polygons = []
    tags = {"building": "yes"}
    osmchange = convert_polygons(lon_lat_polygons, tags)
    osmchange_str = ET.tostring(osmchange, encoding="unicode")
    assert (
        '<osmChange version="0.6" generator="https://github.com/mozilla-ai/osm-ai-helper"><create /><modify /><delete if-unused="true" /></osmChange>'
        in osmchange_str
    )


def assert_equal_tree(tree_a, tree_b):
    def elements_equal(e1, e2):
        if e1.tag != e2.tag:
            raise AssertionError(f"{e1.tag} != {e2.tag}")
        if e1.attrib != e2.attrib:
            raise AssertionError(f"{e1.attrib} != {e2.attrib}")
        if len(e1) != len(e2):
            return AssertionError(f"len(e1) {len(e1)} != len(e2) {len(e2)}")
        return all(elements_equal(c1, c2) for c1, c2 in zip(e1, e2))

    assert elements_equal(tree_a, tree_b)


def test_convert_single_polygon():
    lon_lat_polygons = [[[1.0, 2.0], [3.0, 4.0], [5.0, 6.0], [1.0, 2.0]]]
    osmchange = convert_polygons(lon_lat_polygons)
    expected = ET.fromstring(
        """
        <osmChange version="0.6" generator="https://github.com/mozilla-ai/osm-ai-helper">
            <create>
                <node id="-1" lon="1.0" lat="2.0" version="0" />
                <node id="-2" lon="3.0" lat="4.0" version="0" />
                <node id="-3" lon="5.0" lat="6.0" version="0" />
                <way id="-1" version="0">
                    <nd ref="-1" />
                    <nd ref="-2" />
                    <nd ref="-3" />
                    <nd ref="-1" />
                </way>
            </create>
            <modify />
            <delete if-unused="true" />
        </osmChange>
        """
    )
    assert_equal_tree(osmchange, expected)


def test_convert_multiple_polygons():
    lon_lat_polygons = [
        [[1.0, 2.0], [3.0, 4.0], [5.0, 6.0], [1.0, 2.0]],
        [[10.0, 20.0], [30.0, 40.0], [50.0, 60.0], [01.0, 20.0]],
    ]
    osmchange = convert_polygons(lon_lat_polygons)
    expected = ET.fromstring(
        """
        <osmChange version="0.6" generator="https://github.com/mozilla-ai/osm-ai-helper">
            <create>
                <node id="-1" lon="1.0" lat="2.0" version="0" />
                <node id="-2" lon="3.0" lat="4.0" version="0" />
                <node id="-3" lon="5.0" lat="6.0" version="0" />
                <node id="-4" lon="10.0" lat="20.0" version="0" />
                <node id="-5" lon="30.0" lat="40.0" version="0" />
                <node id="-6" lon="50.0" lat="60.0" version="0" />
                <way id="-1" version="0">
                    <nd ref="-1" />
                    <nd ref="-2" />
                    <nd ref="-3" />
                    <nd ref="-1" />
                </way>
                <way id="-2" version="0">
                    <nd ref="-4" />
                    <nd ref="-5" />
                    <nd ref="-6" />
                    <nd ref="-4" />
                </way>
            </create>
            <modify />
            <delete if-unused="true" />
        </osmChange>
        """
    )
    assert_equal_tree(osmchange, expected)


def test_convert_polygons_with_tags():
    lon_lat_polygons = [
        [[1.0, 2.0], [3.0, 4.0], [5.0, 6.0], [1.0, 2.0]],
        [[10.0, 20.0], [30.0, 40.0], [50.0, 60.0], [01.0, 20.0]],
    ]
    osmchange = convert_polygons(
        lon_lat_polygons,
        tags={"leisure": "swimming_pool", "access": "private", "location": "outdoor"},
    )
    expected = ET.fromstring(
        """
        <osmChange version="0.6" generator="https://github.com/mozilla-ai/osm-ai-helper">
            <create>
                <node id="-1" lon="1.0" lat="2.0" version="0" />
                <node id="-2" lon="3.0" lat="4.0" version="0" />
                <node id="-3" lon="5.0" lat="6.0" version="0" />
                <node id="-4" lon="10.0" lat="20.0" version="0" />
                <node id="-5" lon="30.0" lat="40.0" version="0" />
                <node id="-6" lon="50.0" lat="60.0" version="0" />
                <way id="-1" version="0">
                    <nd ref="-1" />
                    <nd ref="-2" />
                    <nd ref="-3" />
                    <nd ref="-1" />
                    <tag k="leisure" v="swimming_pool" />
                    <tag k="access" v="private" />
                    <tag k="location" v="outdoor" />
                </way>
                <way id="-2" version="0">
                    <nd ref="-4" />
                    <nd ref="-5" />
                    <nd ref="-6" />
                    <nd ref="-4" />
                    <tag k="leisure" v="swimming_pool" />
                    <tag k="access" v="private" />
                    <tag k="location" v="outdoor" />
                </way>
            </create>
            <modify />
            <delete if-unused="true" />
        </osmChange>
        """
    )
    assert_equal_tree(osmchange, expected)
