export const state = () => ({
    datatype: ['radiation', 'uncertainty'],
    timeSeriesCheckedState: ['static', 'mobile'],
    timeSeriesControl: {
        state: 'global',
        localDisabled: true,
    },
    treemapCheckedState: ['static', 'mobile'],
    treemapState: 'treemap1',
    treemapData: {},
    sidTrendChartStyle: 'line',
    playerSpeed: 'hour',
    playerState: false,
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
    timeRange: {},
    sidTrendCharts: [],
    defaultTimeRange: {
        begintime: '2020-04-06 00:00:00',
        endtime: '2020-04-11 00:00:00'
    },
    currentPlayerTime: null,
})

export const getters = {
    datatypeIndex() {
        if (this.datatype == null || this.datatype.length == 0) {
            throw new Error()
        }
        if (this.datatype.length == 2) {
            return 2;
        } else if (this.datatype[0] == 'radiation') {
            return 0;
        } else if (this.datatype[0] == 'uncertainty') {
            return 1;
        }
        throw new Error("")
    }
}

export const mutations = {
    updateDatatype(state, value) {
        state.datatype = value
    },
    updateTimeSeriesCheckedState(state, value) {
        state.timeSeriesCheckedState = value
    },
    updateTimeSeriesControlState(state, value) {
        state.timeSeriesControl.state = value
    },
    updateTimeSeriesControlLocal(state, value) {
        state.timeSeriesControl.localDisabled = value
    },
    updateTreemapCheckedState(state, value) {
        state.treemapCheckedState = value
    },
    updateSidTrendChartStyle(state, value) {
        state.sidTrendChartStyle = value
    },
    updatePlayerSpeed(state, value) {
        state.playerSpeed = value
    },
    updateMapControl(state, value) {
        state.mapControl = value
    },
    updateTreemapData(state, value) {
        state.treemapData = value
    },
    updateTreemapState(state, value) {
        state.treemapState = value
    },
    updateTimeRange(state, value) {
        state.timeRange = value
    },
    updateSidTrendCharts(state, value) {
        state.sidTrendCharts = value
    },
    insertIntoSidTrendCharts(state, value) {
        state.sidTrendCharts.push(value)
    },
    updateCurrentPlayerTime(state, value) {
        state.currentPlayerTime = value
    }

}

import api from '../api/index'
import * as d3 from 'd3'

export const actions = {
    getTreemapDataByTimeRange({ state, commit }, params) {
        if (state.treemapCheckedState.length == 2) {
            api.apiClient.post("/calSensorClusters/", params).then(response => {
                let treemap = {
                    data: response.data,
                    timeRange: params,
                    sensorType: 'both'
                }
                console.log(response)
                commit('updateTreemapData', treemap)
            })
        }
        if (state.treemapCheckedState.length == 1 && state.treemapCheckedState[0] == 'static') {
            axios.post("/calStaticSensorClusters/", params).then(response => {
                let treemap = {
                    state: state.treemapState,
                    data: response.data,
                    timeRange: params,
                    checkedState: state.treemapCheckedState,
                    sensorType: 'static'
                }
                commit('updateTreemapData', treemap)
            })

        }
        if (state.treemapCheckedState.length == 1 && state.treemapCheckedState[0] == 'mobile') {
            axios.post("/calMobileSensorClusters/", params).then(response => {
                let treemap = {
                    state: state.treemapState,
                    data: response.data,
                    timeRange: params,
                    checkedState: state.treemapCheckedState,
                    sensorType: 'mobile'
                }
                commit('updateTreemapData', treemap)
            })

        }
    },
    timeRangeUpdated({ state, commit, dispatch }, params) {
        commit('updateTimeRange', params)
        commit('updateSidTrendCharts', [])
        if (params) {
            commit('updateTimeSeriesControlLocal', false)
            // this.trendChart = null;
            // this.getTrendChartDataByTimeRange(params);
            // this.treemap1 = null;
            // this.treemap2 = null;
            commit('updateTreemapState', 'treemap1')
            dispatch('getTreemapDataByTimeRange', params)
        } else {
            commit('updateTimeSeriesControlLocal', true)
        }
        if (state.playerState) {
            let time = state.timeRange || state.defaultTimeRange;
            commit('updateCurrentPlayerTime', time.begintime)
        }
    },
    defaultSensors({ state, dispatch }, params) {
        // 如果该传感器已经存在，则不添加
        let index = state.sidTrendCharts.findIndex(d => d.category == params.category && d.sid == params.sid)
        if (index != -1) {
            return;
        }
        dispatch('getSidTrendChartData', params)
    },
    getSidTrendChartData({ commit }, params) {
        let parseDate = d3.timeParse('%Y-%m-%d %H:%M:%S');
        api.getTimeSeriesBySid(params)
            .then((response) => {
                let data = response.data.map(function (d) {
                    return {
                        time: parseDate(d.time),
                        lower95: -1.96 * d.standarderror + d.avg,
                        avg: d.avg,
                        upper95: 1.96 * d.standarderror + d.avg,
                        std: d.std
                    };
                });
                let sidtrendChart = {
                    category: params.category,
                    sid: params.sid,
                    timeRange: { begintime: params.begintime, endtime: params.endtime },
                    data: data
                }
                commit('insertIntoSidTrendCharts', sidtrendChart)
            })
    }
}
