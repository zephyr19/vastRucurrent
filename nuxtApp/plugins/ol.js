import Vue from 'vue'
import 'ol/ol.css'
import TileLayer from 'ol/layer/tile'
import VectorTileLayer from 'ol/layer/vectortile'
import VectorTileSource from 'ol/source/vectortile'
import VectorLayer from 'ol/layer/vector'
import VectorSource from 'ol/source/vector'
import XYZSource from 'ol/source/xyz'
import Style from 'ol/style/style'
import Text from 'ol/style/text'
import Fill from 'ol/style/fill'
import Stroke from 'ol/style/stroke'
import MVT from 'ol/format/mvt'
import GeoJSON from 'ol/format/geojson'
import Map from 'ol/map'
import View from 'ol/view'
import Interaction from 'ol/interaction'
import Feature from 'ol/feature'
import Overlay from 'ol/overlay'

const ol = {
    Map: Map,
    View: View,
    Overlay: Overlay,
    Interaction: Interaction,
    layer: {
        Tile: TileLayer,
        Vector: VectorLayer,
        VectorTile: VectorTileLayer
    },
    source: {
        Vector: VectorSource,
        VectorTile: VectorTileSource,
        XYZ: XYZSource
    },
    style: {
        Style: Style,
        // Text: Text,
        Fill: Fill,
        Stroke: Stroke,
    },
    format: {
        MVT: MVT,
        GeoJSON: GeoJSON,
    },
    Feature: Feature
};
Vue.ol = ol