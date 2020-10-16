<template>
  <box title="Individual Sensor Temporal View Settings">
    <el-radio v-model="sidTrendChartStyle" label="line">Line</el-radio>
    <el-radio v-model="sidTrendChartStyle" label="point">Point</el-radio>
  </box>
</template>

<script>
import box from './box.vue'

export default {
  name: 'IndividualSensor',
  components: {
    box,
  },
  computed: {
    sidTrendChartStyle: {
      get() {
        return this.$store.state.sidTrendChartStyle
      },
      set(value) {
        this.$store.commit('updateSidTrendChartStyle', value)
      },
    },
  },
}
</script>

<style></style>
