<template>
  <box title="Animation Settings">
    <el-radio v-model="playerSpeed" label="hour">By 1 hour</el-radio>
    <el-radio v-model="playerSpeed" :disabled="localDisabled" label="minute"
      >By 1 minute</el-radio
    >
    <el-button size="mini" @click="animationPlayer()">{{
      playerState == true ? 'Pause' : 'Play'
    }}</el-button>
  </box>
</template>

<script>
import box from './box.vue'

export default {
  name: 'AnimationSettings',
  components: {
    box,
  },
  computed: {
    playerSpeed: {
      get() {
        return this.$store.state.playerSpeed
      },
      set(value) {
        this.$store.commit('updatePlayerSpeed', value)
      },
    },
    playerState: {
      get() {
        return this.$store.state.playerState
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
