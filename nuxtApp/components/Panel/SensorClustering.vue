<template>
  <box title="Sensor Clustering Treemap View Settings">
    <el-checkbox-group v-model="treemapCheckedState">
      <el-checkbox label="static">Static Sensors (SSs)</el-checkbox>
      <el-checkbox label="mobile">Mobile Sensors (MSs)</el-checkbox>
    </el-checkbox-group>
    <el-button size="mini" @click="getTreemap1()">Back to root</el-button>
  </box>
</template>

<script>
import box from './box.vue'

export default {
  name: 'SensorClustering',
  components: {
    box,
  },
  computed: {
    treemapCheckedState: {
      get() {
        return this.$store.state.treemapCheckedState
      },
      set(value) {
        this.$store.commit('updateTreemapCheckedState', value)
      },
    },
  },
}
</script>

<style></style>
