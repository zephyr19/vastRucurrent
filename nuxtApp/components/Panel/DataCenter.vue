<template>
  <box title="Data Center">
    <el-checkbox-group v-model="datatype">
      <el-checkbox label="radiation">Radiation</el-checkbox>
      <el-checkbox label="uncertainty">Uncertainty</el-checkbox>
    </el-checkbox-group>
  </box>
</template>

<script>
import box from './box.vue'

export default {
  name: 'DataCenter',
  components: {
    box,
  },
  computed: {
    datatype: {
      get() {
        return this.$store.state.datatype
      },
      set(value) {
        this.$store.commit('updateDatatype', value)
      },
    },
  },
}
</script>

<style></style>
