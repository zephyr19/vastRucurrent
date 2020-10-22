<template>
  <div id="openlayers_container">
    <svg id="himarkmap"></svg>
    <div id="popup" class="ol-popup">
      <a href="#" id="popup-closer" class="ol-popup-closer"></a>
      <div id="popup-content"></div>
    </div>
  </div>
</template>
<script>
import CityMap from '../../assets/js/citymap'
import api from '../../api/index.js'
import kriging from '../../assets/js/kriging'
import idw from '../../assets/js/idw'
import * as d3 from 'd3'

export default {
  name: 'Openlayers',
  computed: {
    datatype() {
      return this.$store.state.datatype
    },
    datatypeIndex() {
      return this.$store.getters.datatypeIndex
    },
    mapControl() {
      return this.$store.state.mapControl
    },
  },
  data() {
    return {
      svg: null,
      xScale: null,
      yScale: null,
      svgWidth: 0,
      svgHeight: 0,
      imageExtent: [-120.0, 0, -119.711751, 0.238585], //[left, bottom, right, top]
      zoom: 1.9,
      sid: null,
      timeRange: null,
      mapTimeRange: null,
      dataCollection: {
        staticSensorGridData: null,
        mobileSensorGridData: null,
        mobileSensorReadings: null,
        staticSensorReadings: null,
        mobileUncertaintyGridData: null,
        mobilePathData: null,
      },
      defaultTimeRange: {
        begintime: '2020-04-06 00:00:00',
        endtime: '2020-04-11 00:00:00',
      },
      popup: {
        container: null,
        content: null,
        closer: null,
      },
    }
  },
  mounted() {
    this.$nextTick(() => {
      this.loadMap()
    })
  },
  methods: {
    loadMap() {
      let container = document.querySelector('#openlayers_container')
      let parentNode = container.parentNode
      this.svgWidth = parentNode.clientWidth
      this.svgHeight = parentNode.clientHeight

      // var imgHeight = 995,
      var width = this.svgWidth,
        height = this.svgHeight, // Dimensions of cropped region
        translate0 = [0, 0],
        scale0 = 1 // Initial offset & scale

      let svg = d3
        .select('#himarkmap')
        .attr('width', width + 'px')
        .attr('height', height + 'px')

      svg
        .append('rect')
        .attr('class', 'overlay')
        .attr('width', width + 'px')
        .attr('height', height + 'px')

      svg = svg
        .append('g')
        .attr('transform', 'translate(' + translate0 + ')scale(' + scale0 + ')')
        .call(
          d3
            .zoom()
            .scaleExtent([1, 40])
            .on('zoom', (e) => {
              svg.attr(
                'transform',
                'translate(' +
                  d3.event.transform.x +
                  ', ' +
                  d3.event.transform.y +
                  ')scale(' +
                  d3.event.transform.k +
                  ')'
              )
            })
        )
        .append('g')

      svg
        .append('image')
        .attr('width', '100%')
        .attr('height', '100%')
        .attr('xlink:href', './img/StHimarkMapRoad.png')
      this.svg = svg
      this.xScale = d3
        .scaleLinear()
        .domain([this.imageExtent[0], this.imageExtent[2]])
        .range([0, width])
      this.yScale = d3
        .scaleLinear()
        .domain([this.imageExtent[1], this.imageExtent[3]])
        .range([height, 0])
      this.drawStaticPointLayer()
      // this.drawMobilePointLayer()
      this.drawTilesLayer()
    },
    drawTilesLayer() {
      let svg = this.svg
      let xScale = this.xScale
      let yScale = this.yScale
      api
        .getMobileIdwDataByTimeRange(this.timeRange || this.defaultTimeRange)
        .then((res) => {
          console.log(res)
          this.dataCollection.mobileSensorGridData = res.data
          render(res.data)
        })
      function render(idwdata) {
        let colorScale = d3
          .scaleLinear()
          .domain([25, 80])
          .range(['rgb(0,255,0)', 'rgb(255,0,0)'])
        idwdata.forEach((d) => {
          svg
            .append('rect')
            .attr('x', xScale(d.lngEx[0]))
            .attr('y', yScale(d.latEx[0]))
            // .attr('width', xScale(Math.abs(d.lngEx[0] - d.lngEx[1])))
            // .attr('height', yScale(Math.abs(d.latEx[0] - d.latEx[1])))
            .attr('width', Math.abs(xScale(d.lngEx[0]) - xScale(d.lngEx[1])))
            .attr('height', Math.abs(yScale(d.latEx[0]) - yScale(d.latEx[1])))
            .attr('fill', colorScale(d.mean))
            .attr('stroke', 'white')
            .attr('opacity', '0.3')
        })
      }
    },
    drawMobilePointLayer() {
      //BUG: POST ERROR
      let svg = this.svg
      // let endtime = this.defaultTimeRange.endtime
      let endtime = this.timeRange.endtime
      api
        .getLastCoordByTimeRange({
          endtime:
            endtime.substring(0, 17) +
            Math.floor(new Date(endtime).getSeconds() / 5) * 5,
        })
        .then((res) => {
          console.log(res)
          let points = res.data
          points.forEach((d) => {
            let lon = parseFloat(d.long),
              lat = parseFloat(d.lat)
            console.log(lon + ' ' + this.xScale(lon))
            svg
              .append('image')
              .attr('xlink:href', './img/static.png')
              .attr('width', '20px')
              .attr('height', '20px')
              .attr('x', this.xScale(lon))
              .attr('y', this.yScale(lat))
          })
        })
    },
    drawStaticPointLayer() {
      let svg = this.svg
      d3.csv('./data/StaticSensorLocations.csv').then((csvdata) => {
        csvdata.forEach((d) => {
          let lon = parseFloat(d.long),
            lat = parseFloat(d.lat)
          svg
            .append('image')
            .attr('xlink:href', './img/static.png')
            .attr('width', '20px')
            .attr('height', '20px')
            .attr('x', this.xScale(lon))
            .attr('y', this.yScale(lat))
        })
      })
      // svg
      //   .append('g')
      //   .selectAll('image')
      //   .data(data)
      //   .append('image')
      //   .attr('xlink:href', './img/static.png')
      //   .transform()
    },
  },
  watch: {
    zoom(newValue, oldValue) {
      if (this.u_pie_check) {
        this.clearPies()
        this.drawPies()
      }
      if (this.mapControl.r_mi_idw_check) {
        this.map.removeLayer(this.layers.SRLayer)
        this.layers.SRLayer = null
        this.drawSRLayer()
      }
    },
    mapControl: {
      handler(newValue, oldValue) {
        if (this.image !== this.mapControl.image) {
          this.map.removeLayer(this.layers.imageLayer)
          this.layers.imageLayer = new Image({
            source: new ImageStatic({
              url: require(`../../assets/img/${this.mapControl.image}.png`),
              imageExtent: this.imageExtent,
            }),
          })
          this.image = this.mapControl.image
          this.map.addLayer(this.layers.imageLayer)
          this.clearLayers()
        }
        if (this.timeRange == null) {
          return
        }
        if (
          this.mapControl.icon_s_check &&
          this.layers.staticPointLayer == null
        ) {
          this.drawStaticPointLayer()
        }
        if (
          this.mapControl.icon_m_check &&
          this.layers.mobilePointLayer == null
        ) {
          this.drawMobilePointLayer()
        }
        if (
          this.mapControl.inconsistency_check &&
          this.layers.inconsistencyLayer == null
        ) {
          this.drawInconsistencyLayer()
        }

        if (this.datatype.length == 2) {
          //radiation和uncertainty都选中时的插值
          if (
            this.mapControl.si_idw_check &&
            this.layers.staticIdwLayer == null
          ) {
            this.drawIdwRUSLayer()
          }
          if (
            this.mapControl.mi_idw_check &&
            this.layers.mobileIdwLayer == null
          ) {
            this.drawIdwRUMLayer()
          }
        }
        if (this.datatype.length == 1 && this.datatype[0] == 'radiation') {
          if (
            this.mapControl.si_idw_check &&
            this.layers.staticIdwLayer == null
          ) {
            this.drawIdwSLayer()
          }
          if (
            this.mapControl.mi_idw_check &&
            this.layers.mobileIdwLayer == null
          ) {
            this.drawIdwMLayer()
          }
        }
        if (this.datatype.length == 1 && this.datatype[0] == 'uncertainty') {
          if (
            this.mapControl.si_idw_check &&
            this.layers.staticIdwLayer == null
          ) {
            this.drawIdwUncertaintySLayer()
          }
          if (
            this.mapControl.mi_idw_check &&
            this.layers.mobileIdwLayer == null
          ) {
            this.drawIdwUncertaintyMLayer()
          }
        }
        this.updateLayers()
      },
      deep: true,
    },
    datatype(n, o) {
      if (this.timeRange == null) {
        return
      }
      this.clearLayers()
      if (
        this.mapControl.icon_s_check &&
        this.layers.staticPointLayer == null
      ) {
        this.drawStaticPointLayer()
      }
      if (
        this.mapControl.icon_m_check &&
        this.layers.mobilePointLayer == null
      ) {
        this.drawMobilePointLayer()
      }
      if (
        this.mapControl.inconsistency_check &&
        this.layers.inconsistencyLayer == null
      ) {
        this.drawInconsistencyLayer()
      }

      if (this.datatype.length == 2) {
        //radiation和uncertainty都选中时的插值
        if (
          this.mapControl.si_idw_check &&
          this.layers.staticIdwLayer == null
        ) {
          this.drawIdwRUSLayer()
        }
        if (
          this.mapControl.mi_idw_check &&
          this.layers.mobileIdwLayer == null
        ) {
          this.drawIdwRUMLayer()
        }
      }
      if (this.datatype.length == 1 && this.datatype[0] == 'radiation') {
        if (
          this.mapControl.si_idw_check &&
          this.layers.staticIdwLayer == null
        ) {
          this.drawIdwSLayer()
        }
        if (
          this.mapControl.mi_idw_check &&
          this.layers.mobileIdwLayer == null
        ) {
          this.drawIdwMLayer()
        }
      }
      if (this.datatype.length == 1 && this.datatype[0] == 'uncertainty') {
        if (
          this.mapControl.si_idw_check &&
          this.layers.staticIdwLayer == null
        ) {
          this.drawIdwUncertaintySLayer()
        }
        if (
          this.mapControl.mi_idw_check &&
          this.layers.mobileIdwLayer == null
        ) {
          this.drawIdwUncertaintyMLayer()
        }
      }
      this.updateLayers()
    },
  },
  computed: {
    coords: function () {
      return [
        [
          [this.imageExtent[0], this.imageExtent[3]],
          [this.imageExtent[2], this.imageExtent[3]],
          [this.imageExtent[2], this.imageExtent[1]],
          [this.imageExtent[0], this.imageExtent[1]],
        ],
      ]
    },
  },
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
#openlayers_container {
  height: 100%;
  /* background-image: url('../../assets/img/StHimarkMapRoad.png'); */
}
#himarkmap {
  width: 100%;
  height: 100%;
  /* margin-top: 5px; */
  /* position: absolute;
  top: 10%; */
}
.overlay {
  fill: none;
  pointer-events: all;
}
.el-tabs {
  height: 30px;
}
.ol-popup {
  position: absolute;
  background-color: white;
  -webkit-filter: drop-shadow(0 1px 4px rgba(0, 0, 0, 0.2));
  filter: drop-shadow(0 1px 4px rgba(0, 0, 0, 0.2));
  padding: 15px;
  border-radius: 10px;
  border: 1px solid #cccccc;
  bottom: 12px;
  left: -50px;
  min-width: 200px;
  font-size: 12px;
}
.ol-popup:after,
.ol-popup:before {
  top: 100%;
  border: solid transparent;
  content: ' ';
  height: 0;
  width: 0;
  position: absolute;
  pointer-events: none;
}
.ol-popup:after {
  border-top-color: white;
  border-width: 10px;
  left: 48px;
  margin-left: -10px;
}
.ol-popup:before {
  border-top-color: #cccccc;
  border-width: 11px;
  left: 48px;
  margin-left: -11px;
}
.ol-popup-closer {
  text-decoration: none;
  position: absolute;
  top: 2px;
  right: 8px;
}
.ol-popup-closer:after {
  content: '✖';
}
</style>
