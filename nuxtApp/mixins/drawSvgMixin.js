import * as d3 from 'd3'

export const drawSvgMixin = {
    inheritAttrs: false,
    methods: {
        loadChart(id) {
            this.selfAdaptionSvgSize(id)
            this.drawSvg()
            this.drawChart()
        },
        selfAdaptionSvgSize(id) {
            let parentNode = document.querySelector(id).parentNode
            this.svgWidth = parentNode.clientWidth
            this.svgHeight = parentNode.clientHeight
            d3.select(id).style('position', 'relative')
        },
        drawSvg() {
            this.svg = d3
                .select(`#${this.cid} .times_series_chart`)
                .append('svg')
                .attr('width', this.svgWidth)
                .attr('height', this.svgHeight)
        },
    },
};