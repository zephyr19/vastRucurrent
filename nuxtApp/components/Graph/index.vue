<template>
  <div class="graph">
    <time-series-chart :cid="`time_series_chart_container`" />
  </div>
</template>

<script>
import TimeSeriesChart from './TimeSeriesChart.vue'
import test from '../../api/test.js'

export default {
  components: {
    TimeSeriesChart,
  },
  created() {
    test.getEvents().then((res) => {
      console.log(res)
    })
  },
}
</script>

<style></style>
