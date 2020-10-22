import axios from 'axios'

const apiClient = axios.create({
    baseURL: `http://localhost:8000`,
    withCredentials: false, // This is the default
    headers: {
        Accept: 'application/json',
        'Content-Type': 'application/json'
    }
})

export default {
    apiClient: apiClient,
    getEvents() {
        return apiClient.get('/testdb')
    },
    getMobileIdwDataByTimeRange(params) {
        return apiClient.post("/getMobileIdwDataByTimeRange/", params)
    },
    getLastCoordByTimeRange(params) {
        return apiClient.post('/getLastCoordByTimeRange/', params)
    },
    getTreemapDataByTimeRange(params) {
        // if (this.treemapCheckedState.length == 2) {
        return apiClient.post("/calSensorClusters/", params)
        // }
        // if (this.treemapCheckedState.length == 1 && this.treemapCheckedState[0] == 'static') {
        //     axios.post("/calStaticSensorClusters/", params).then(response => {
        //         this.treemap1 = {
        //             state: this.treemapState,
        //             data: response.data,
        //             timeRange: params,
        //             checkedState: this.treemapCheckedState,
        //             sensorType: 'static'
        //         }
        //     })

        // }
        // if (this.treemapCheckedState.length == 1 && this.treemapCheckedState[0] == 'mobile') {
        //     axios.post("/calMobileSensorClusters/", params).then(response => {
        //         this.treemap1 = {
        //             state: this.treemapState,
        //             data: response.data,
        //             timeRange: params,
        //             checkedState: this.treemapCheckedState,
        //             sensorType: 'mobile'
        //         }
        //     })

        // }


    },
    getTimeSeriesBySid(params) {
        return apiClient.post('/calTimeSeriesBySid/', params)
    },
    getSrBySid(params) {
        return apiClient.post("/findSrBySid/", params)
    }
}