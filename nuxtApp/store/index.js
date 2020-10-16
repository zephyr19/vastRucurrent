export const state = () => ({
    datatype: ['radiation', 'uncertainty'],
    timeSeriesCheckedState: ['static', 'mobile'],
    timeSeriesControl: {
        state: 'global',
        localDisabled: true,
    },
    treemapCheckedState: ['static', 'mobile'],
    sidTrendChartStyle: null,
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
})

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
    }

}

export const actions = {
    timeRangeUpdated(params) {
        this.timeRange = params;
        this.sidTrendCharts = [];
        if (params) {
            this.timeSeriesControl.localDisabled = false;
            // this.timeSeriesControl.state = "local";
            this.trendChart = null;
            this.getTrendChartDataByTimeRange(params);
            this.treemap1 = null;
            this.treemap2 = null;
            this.treemapState = 'treemap1';
            this.getTreemapDataByTimeRange(params);
        } else {
            this.timeSeriesControl.localDisabled = true;
        }
        if (!this.playerState) {
            let time = this.timeRange || this.defaultTimeRange;
            this.currentPlayerTime = time.begintime;
        }
    }
}
