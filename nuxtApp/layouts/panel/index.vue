<template>
  <el-scrollbar
    wrapClass="yf-container"
    viewClass="yf-content"
    wrapStyle="color:'#fff';fontSize:'16px';"
    viewStyle="color:'#fff';fontSize:'16px';"
    :native="false"
    :noresize="true"
  >
    <div class="control-header">Data Center</div>
    <div class="control-content">
      <el-checkbox-group v-model="datatype">
        <el-checkbox label="radiation">Radiation</el-checkbox>
        <el-checkbox label="uncertainty">Uncertainty</el-checkbox>
      </el-checkbox-group>
    </div>
    <div class="control-header">Overall Radiation Trend View Settings</div>
    <div class="control-content">
      <el-checkbox-group v-model="timeSeriesCheckedState">
        <el-checkbox label="static">Static Sensors (SSs)</el-checkbox>
        <el-checkbox label="mobile">Mobile Sensors (MSs)</el-checkbox>
      </el-checkbox-group>
      <el-radio v-model="timeSeriesControl.state" label="global"
        >By 1 hour</el-radio
      >
      <el-radio
        v-model="timeSeriesControl.state"
        :disabled="timeSeriesControl.localDisabled"
        label="local"
        >By 1 minute</el-radio
      >
    </div>
    <div class="control-header">Sensor Clustering Treemap View Settings</div>
    <div class="control-content">
      <el-checkbox-group v-model="treemapCheckedState">
        <el-checkbox label="static">Static Sensors (SSs)</el-checkbox>
        <el-checkbox label="mobile">Mobile Sensors (MSs)</el-checkbox>
      </el-checkbox-group>
      <el-button size="mini" @click="getTreemap1()">Back to root</el-button>
    </div>
    <div class="control-header">Individual Sensor Temporal View Settings</div>
    <div class="control-content">
      <el-radio v-model="sidTrendChartStyle" label="line">Line</el-radio>
      <el-radio v-model="sidTrendChartStyle" label="point">Point</el-radio>
    </div>
    <div class="control-header">Gis View Settings</div>
    <div class="control-content">
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
      <el-checkbox v-model="mapControl.icon_s_check"
        >Static Sensors (SSs)</el-checkbox
      >
      <img :src="require('../../assets/img/static.png')" alt="" width="20px;" />
      <el-checkbox v-model="mapControl.icon_m_check"
        >Mobile Sensors (MSs)</el-checkbox
      >
      <img :src="require('../../assets/img/mobile.png')" alt="" width="20px;" />
      <el-checkbox v-model="mapControl.si_idw_check"
        >Static Interpolation</el-checkbox
      ><el-checkbox v-model="mapControl.mi_idw_check"
        >Mobile Interpolation</el-checkbox
      >
    </div>
    <div class="control-header">Animation Settings</div>
    <div class="control-content">
      <el-radio v-model="playerSpeed" label="hour">By 1 hour</el-radio>
      <el-radio
        v-model="playerSpeed"
        :disabled="timeSeriesControl.localDisabled"
        label="minute"
        >By 1 minute</el-radio
      >
      <el-button size="mini" @click="animationPlayer()">{{
        playerState == true ? 'Pause' : 'Play'
      }}</el-button>
    </div>
    <div class="control-header">Uncertainty Settings</div>
    <div class="control-content">
      <div class="input-ele-group first">
        <label class="bold">Uncertainty index system</label>
      </div>
      <table>
        <tr v-for="(item, i) in uncertaintyIndex">
          <td width="240px">U{{ i }}: {{ item.name }}</td>
          <td width="300px">
            weight:
            <input
              type="text"
              style="width: 30px; text-align: center"
              :value="item.weight"
            />
          </td>
        </tr>
      </table>
      <div class="control-content">
        <div class="input-ele-group first">
          <label class="bold">Uncertainty levels</label>
        </div>
        <ul>
          <li v-for="(item, i) in uncertaintyLevels" :key="i">
            Level {{ i + 1 }}:
            <i v-for="j in i + 1" class="el-icon-star-on"></i>
            {{ item }}
          </li>
        </ul>
      </div>
    </div>
  </el-scrollbar>
</template>

<script>
export default {
  name: 'panel',
  data() {
    return {
      srScatterVisible: false,
      datatype: ['radiation', 'uncertainty'],
      timeSeriesControl: {
        state: 'global',
        localDisabled: true,
      },
      timeSeriesCheckedState: ['static', 'mobile'],
      treemapCheckedState: ['static', 'mobile'],
      treemapState: 'treemap1',
      mapControl: {
        icon_m_check: false,
        icon_s_check: false,
        si_idw_check: false,
        mi_idw_check: false,
        inconsistency_check: false,
        image: 'StHimarkMapRoad',
      },
      mapImages: [
        'StHimarkMapRoad',
        'StHimarkMapBlank',
        'StHimarkMapPoi',
        'StHimarkMapHouse',
      ],
      uncertaintyIndex: [
        {
          name: 'Inconsistency',
          weight: 1,
        },
        {
          name: 'Credibility',
          weight: 1,
        },
        {
          name: 'Precision',
          weight: 1,
        },
        {
          name: 'Data completeness',
          weight: 1,
        },
      ],
      uncertaintyLevels: ['low', 'guarded', 'elevated', 'high', 'severe'],
      trendChart: null,
      sidTrendCharts: [],
      sidTrendChartStyle: null,
      treemap1: null,
      treemap2: null,
      timeRange: null,
      defaultTimeRange: {
        begintime: '2020-04-06 00:00:00',
        endtime: '2020-04-11 00:00:00',
      },
      playerState: false,
      playerSpeed: 'hour',
      currentPlayerTime: null,
      inteval: null,
    }
  },
}
</script>

<style>
.control-header {
  background-color: #ccc;
  line-height: 40px;
  padding-left: 10px;
  font-size: 16px;
  font-weight: bold;
}

.control-content {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  padding: 14px 10px;
}
.control-content img {
  width: 15px;
}
.input-ele {
  width: 50%;
  display: inline-block;
}
.control-content .input-ele-group,
.input-ele,
label {
  height: 18px;
  line-height: 18px;
}
.control-content input.button,
select.select {
  height: 18px;
  line-height: 18px;
}
.control-content label {
  vertical-align: middle;
}
</style>
