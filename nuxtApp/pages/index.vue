<template>
  <div class="container">
    <panel />
    <graph />
    <!-- <test /> -->
  </div>
</template>

<script>
import 'element-ui/lib/theme-chalk/display.css'
import Panel from '../components/Panel/index.vue'
import Graph from '../components/Graph/index.vue'
// import test from '../components/test.vue'

export default {
  name: 'app',
  components: {
    Panel,
    Graph,
    // test,
  },
  data() {
    return {
      srScatterVisible: false,
      treemapState: 'treemap1',
      trendChart: null,
      sidTrendCharts: [],
      treemap1: null,
      treemap2: null,
      timeRange: null,
      defaultTimeRange: {
        begintime: '2020-04-06 00:00:00',
        endtime: '2020-04-11 00:00:00',
      },
      playerState: false,
      currentPlayerTime: null,
      inteval: null,
    }
  },
}
</script>

<style>
.container {
  height: 100vh;
  width: 100%;
  display: flex;
}

.panel {
  width: 340px;
}

.graph {
  width: 100%;
  height: 340px;
}
</style>
