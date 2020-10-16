<template>
  <box title="Overall Radiation Trend View Settings">
    <el-checkbox-group v-model="timeSeriesCheckedState">
      <el-checkbox label="static">Static Sensors (SSs)</el-checkbox>
      <el-checkbox label="mobile">Mobile Sensors (MSs)</el-checkbox>
    </el-checkbox-group>
    <el-radio v-model="state" label="global">By 1 hour</el-radio>
    <el-radio v-model="state" :disabled="localDisabled" label="local"
      >By 1 minute</el-radio
    >
  </box>
</template>

<script>
import box from './box.vue'

export default {
  name: 'RadiationTrend',
  components: {
    box,
  },
  computed: {
    timeSeriesCheckedState: {
      get() {
        return this.$store.state.timeSeriesCheckedState
      },
      set(value) {
        this.$store.commit('updateTimeSeriesCheckedState', value)
      },
    },
    state: {
      get() {
        return this.$store.state.timeSeriesControl.state
      },
      set(value) {
        this.$store.commit('updateTimeSeriesControlState', value)
      },
    },
    localDisabled: {
      get() {
        return this.$store.state.timeSeriesControl.localDisabled
      },
      set(value) {
        this.$store.commit('updateTimeSeriesControlLocal', value)
      },
    },
  },
}
</script>

<style></style>
