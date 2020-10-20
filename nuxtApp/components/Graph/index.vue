<template>
  <div class="graph">
    <div class="top">
      <time-series-chart class="top" :cid="`time_series_chart_container`" />
    </div>
    <el-row class="bottom">
      <el-col :span="9" class="bottom_left">
        <div class="grid-content bottom_left_top">
          <treemap :cid="`treemap-container`"></treemap>
        </div>
        <div class="grid-content bottom_left_bottom">
          <div
            v-for="(item, index) in sidTrendCharts"
            :key="index"
            class="innerdiv"
          >
            <sid-trend-chart
              :cid="`trend_chart_container_${index}`"
              :originData="item"
              :componentStyle="sidTrendChartStyle"
            ></sid-trend-chart>
          </div>
        </div>
      </el-col>
    </el-row>
  </div>
</template>

<script>
import TimeSeriesChart from './TimeSeriesChart.vue'
import Treemap from './Treemap.vue'
import SidTrendChart from './SidTrendChart.vue'
import api from '../../api/index.js'

export default {
  components: {
    TimeSeriesChart,
    Treemap,
    SidTrendChart,
  },
  computed: {
    // datatype() {
    //   return this.$store.state.datatype
    // },
  },
  created() {
    api.getEvents().then((res) => {
      console.log(res)
    })
  },
}
</script>

<style scoped>
.graph {
  width: 100%;
  height: 100%;
}

.top {
  height: 16%;
}

.bottom {
  height: 84%;
}

.bottom_left {
  height: 100%;
}

.bottom_left_top {
  height: 60%;
}
</style>
