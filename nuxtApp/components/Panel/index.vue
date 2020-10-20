<template>
  <el-scrollbar
    class="panel hidden-md-and-down"
    wrapClass="yf-container"
    viewClass="yf-content"
    wrapStyle="color:'#fff';fontSize:'16px';"
    viewStyle="color:'#fff';fontSize:'16px';"
    :native="false"
    :noresize="true"
  >
    <data-center />
    <radiation-trend />
    <sensor-clustering />
    <individual-sensor />
    <gis-view />
    <animation-settings />
    <uncertainty-settings />
  </el-scrollbar>
</template>

<script>
import DataCenter from './DataCenter.vue'
import RadiationTrend from './RadiationTrend.vue'
import SensorClustering from './SensorClustering.vue'
import IndividualSensor from './IndividualSensor.vue'
import GisView from './GisView.vue'
import AnimationSettings from './AnimationSettings.vue'
import UncertaintySettings from './UncertaintySettings.vue'

export default {
  components: {
    DataCenter,
    RadiationTrend,
    SensorClustering,
    IndividualSensor,
    GisView,
    AnimationSettings,
    UncertaintySettings,
  },
}
</script>

<style></style>
