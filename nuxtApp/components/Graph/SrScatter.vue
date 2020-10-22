<template>
  <div :id="cid">
    <div class="scatterControl">
      <span>{{ category == 'static' ? 'SS' : 'MS' }}-{{ sid }}</span>
      <span style="margin-left: 15px">min: {{ minValue }}</span>
      <span style="margin-left: 15px">max: {{ maxValue }}</span> &nbsp;<br />
      filter:
      <el-input
        size="mini"
        v-model="minInput"
        placeholder="min"
        @change="minChanged"
      ></el-input>
      &nbsp;<span>-</span>&nbsp;
      <el-input
        size="mini"
        v-model="maxInput"
        placeholder="max"
        @change="maxChanged"
      ></el-input>
    </div>
    <div class="scatterplot"></div>
  </div>
</template>

<script>
import * as d3 from 'd3'
import api from '../../api/index.js'
export default {
  name: 'SrScatter',
  props: {
    cid: String,
    category: String,
    sid: [String, Number],
  },
  data() {
    return {
      minInput: 0,
      maxInput: 60,
      minValue: null,
      maxValue: null,
      svgWidth: 0,
      svgHeight: 0,
    }
  },
  mounted() {
    this.$nextTick(() => {
      this.loadChart()
    })
  },
  methods: {
    loadChart() {
      this.selfAdaptionSvgSize()
      this.drawSvg()
      this.drawScatter()
    },
    selfAdaptionSvgSize() {
      let parentNode = document.querySelector(`#${this.cid}`).parentNode
      let parentHeight = parentNode.clientHeight
      let control = document.querySelector(`#${this.cid} .scatterControl`)
      this.svgWidth = control.clientWidth
      this.svgHeight = parentHeight - control.clientHeight
    },
    drawSvg() {
      this.svg = d3
        .select(`#${this.cid} .scatterplot`)
        .append('svg')
        .attr('width', this.svgWidth)
        .attr('height', this.svgHeight)
    },
    drawScatter() {
      let margin = { top: 5, right: 15, bottom: 20, left: 30 }
      let width = this.svgWidth - margin.left - margin.right
      let height = this.svgHeight - margin.top - margin.bottom

      let container = d3.select(`#${this.cid} .scatterplot`)

      // Init g
      let g = this.svg
        .append('g')
        .attr('transform', `translate(${margin.left}, ${margin.top})`)

      // Init Canvas
      let canvasChart = container
        .append('canvas')
        .attr('width', width)
        .attr('height', height)
        .style('margin-left', margin.left + 'px')
        .style('margin-top', margin.top + 'px')
        .attr('class', 'canvas-plot')

      let context = canvasChart.node().getContext('2d')
      let _this = this
      api
        .getSrBySid({
          category: this.category,
          sid: this.sid,
        })
        .then(function (response) {
          let responseData = response.data

          _this.maxValue = d3.max(responseData, (d) => d.value)
          _this.minValue = d3.min(responseData, (d) => d.value)

          // Init Scales
          let x = d3
            .scaleTime()
            .domain([new Date(2020, 3, 6), new Date(2020, 3, 11)])
            .range([0, width])
          let y = d3
            .scaleLinear()
            .domain([0, _this.maxInput])
            .range([height, 0])

          // Init Axis
          let tmp = null
          let xAxis = d3
            .axisBottom(x)
            .ticks(d3.timeHour.every(6))
            .tickFormat((d, i) => {
              var formatMonth = d3.timeFormat('%B %d')
              if (d.getHours() % 24 == 0) {
                return formatMonth(d)
              } else {
                return `${d.getHours()}:00`
              }
              tmp = d
            })
          let yAxis = d3.axisLeft(y)

          // // Add Axis
          let gxAxis = g
            .append('g')
            .attr('class', 'x axis ')
            .attr('transform', `translate(0, ${height})`)
            .call(xAxis)

          let gyAxis = g.append('g').attr('class', 'y axis').call(yAxis)

          // Draw on canvas
          responseData.forEach((point) => {
            drawPoint(point)
          })

          function drawPoint(point) {
            context.beginPath()
            // context.fillStyle = pointColor;
            const px = x(new Date(point.timestamp))
            const py = y(point.value)

            context.fillStyle = 'steelblue'
            context.arc(px, py, 1, 0, 2 * Math.PI, true)
            context.fill()
          }
        })
        .catch(function (error) {
          console.log(error)
        })
    },
    maxChanged(value) {
      this.maxInput = value
      d3.select(`#${this.cid} .scatterplot svg`).selectAll('g').remove()
      d3.select(`#${this.cid} .scatterplot`).selectAll('canvas').remove()
      this.drawScatter()
    },
    minChanged(value) {
      this.minValue = value
      d3.select(`#${this.cid} .scatterplot svg`).selectAll('g').remove()
      d3.select(`#${this.cid} .scatterplot`).selectAll('canvas').remove()
      this.drawScatter()
    },
  },
  // watch: {
  //   category(n, o) {
  //     console.log(n)
  //     d3.select(`#${this.cid} .scatterplot svg`).selectAll('g').remove();
  //     d3.select(`#${this.cid} .scatterplot`).selectAll('canvas').remove();
  //     this.drawScatter();
  //   },
  //   sid(n, o) {
  //     console.log(n)
  //     d3.select(`#${this.cid} .scatterplot svg`).selectAll('g').remove();
  //     d3.select(`#${this.cid} .scatterplot`).selectAll('canvas').remove();
  //     this.drawScatter();
  //   }
  // }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style>
.scatterplot {
  position: relative;
  margin-top: 10px;
}
.scatterplot .canvas-plot {
  position: absolute;
  left: 0;
  top: 0;
}
.scatterControl .el-input {
  width: 60px;
}
.scatterControl span {
  font-size: 12px;
}
</style>
