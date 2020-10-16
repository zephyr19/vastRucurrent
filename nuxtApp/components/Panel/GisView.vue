<template>
  <box title="Gis View Settings">
    <label>Map layers:</label>
    <el-select
      size="mini"
      class="select"
      style="margin-left: 5px"
      v-model="mapControl.image"
      placeholder=""
      @change="changeMapImage"
    >
      <el-option
        v-for="(item, index) in mapImages"
        :key="index"
        :label="item"
        :value="item"
      >
      </el-option>
    </el-select>
    <el-checkbox-group v-model="mapControl">
      <el-checkbox label="icon_s_check">Static Sensors (SSs)</el-checkbox>
      <img :src="require('../../assets/img/static.png')" alt="" width="20px;" />
      <el-checkbox label="icon_m_check">Mobile Sensors (MSs)</el-checkbox>
      <img :src="require('../../assets/img/mobile.png')" alt="" width="20px;" />
      <el-checkbox label="si_idw_check">Static Interpolation</el-checkbox
      ><el-checkbox label="mi_idw_check">Mobile Interpolation</el-checkbox>
    </el-checkbox-group>
  </box>
</template>

<script>
import box from './box.vue'

export default {
  name: 'GisView',
  components: {
    box,
  },
  computed: {
    mapControl: {
      get() {
        return this.$store.state.mapControl
      },
      set(value) {
        this.$store.commit('updateMapControl', value)
      },
    },
    mapImages: {
      get() {
        return this.$store.state.mapImages
      },
    },
  },
}
</script>

<style></style>
