const path = require('path')
import * as d3 from 'd3';

class CityMap {

  constructor(longitudeRange, latitudeRange) {
    this.longitudeRange = longitudeRange || [-120.0, -119.711751];
    this.latitudeRange = latitudeRange || [0.238585, 0.0];
    this.width = null;
    this.height = null;
    this.data = null;
    this.girdsize = null;
    this.gridMatrix = [];
  }

  setMapSize(width, height) {
    this.width = width;
    this.height = height;
  }

  loadData(data) {
    this.data = data;
  }

  setGridSize(girdsize) {
    this.girdsize = girdsize;
  }

  setGridMatrix() {
    let n = Math.ceil(Math.abs(this.width / (this.longitudeRange[1] - this.longitudeRange[0])))
    let m = Math.ceil(Math.abs(this.height / (this.latitudeRange[1] - this.latitudeRange[0])))
    
    return [n, m];
  }

  assignGird(longitude, latitude) {

  }

  mappingToCoordinate(latitude, longitude) {
    /**
     * 将经纬度映射成坐标
     */
    let xScale = d3.scaleLinear().domain(this.longitudeRange).range([0, this.width]);
    let yScale = d3.scaleLinear().domain(this.latitudeRange).range([0, this.height]);
    return [xScale(longitude), yScale(latitude)];
  }

  mappingToPostion(x, y) {
    /**
     * 将位置映射成经纬度
     * Returns [纬度， 经度]
     */
    let xScale = d3.scaleLinear().domain(this.longitudeRange).range([0, this.width]);
    let yScale = d3.scaleLinear().domain(this.latitudeRange).range([0, this.height]);
    return [yScale.invert(y), xScale.invert(x)];
  }
}

export default CityMap
