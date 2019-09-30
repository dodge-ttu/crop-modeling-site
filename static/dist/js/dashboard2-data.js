/*Dashboard2 Init*/

// Django template tag creates the json allsites object
var datetimehist = JSON.parse(document.getElementById('datetimehist').textContent);
var temphist = JSON.parse(document.getElementById('temphist').textContent);
var windhist = JSON.parse(document.getElementById('windhist').textContent);
var presshist = JSON.parse(document.getElementById('presshist').textContent);
var etohist = JSON.parse(document.getElementById('etohist').textContent);
var accum_etohist = JSON.parse(document.getElementById('accum_etohist').textContent);
var rains_1hhist = JSON.parse(document.getElementById('rains_1hhist').textContent);
var gduhist = JSON.parse(document.getElementById('gdushist').textContent);
var accum_gduhist = JSON.parse(document.getElementById('accum_gduhist').textContent);

"use strict"; 
$(document).ready(function() {

     if($('#area_chart_accum_gdu').length > 0) {

        // based on prepared DOM, initialize echarts instance
        var myChart_accum_gdu = echarts.init(document.getElementById('area_chart_accum_gdu'));

        var option_accum_gdu = {
            tooltip: {
                trigger: 'axis',
                position: function (pt) {
                    return [pt[0], '10%'];
                }
            },
            toolbox: {
                feature: {
                    dataZoom: {
                        yAxisIndex: 'none'
                    },
                    restore: {},
                    saveAsImage: {}
                }
            },
            xAxis: {
                type: 'category',
                boundaryGap: false,
                data: datetimehist,
            },
            yAxis: {
                type: 'value',
            },
            series: [
                {
                    name: 'AccumGDU',
                    type: 'line',
                    smooth: true,
                    symbol: 'circle',
                    symbolSize: 7,
                    sampling: 'average',
                    lineStyle: {
                        color: '#233c46',
                        width: 1,
                    },
                    itemStyle: {
                        color: '#233c46',
                    },
                    data: accum_gduhist
                }
            ]
        };
    }

    // use configuration item and data specified to show chart
    myChart_accum_gdu.setOption(option_accum_gdu);

     if($('#area_chart_gdu').length > 0) {

        // based on prepared DOM, initialize echarts instance
        var myChart_gdu = echarts.init(document.getElementById('area_chart_gdu'));

        var option_gdu = {
            tooltip: {
                trigger: 'axis',
                position: function (pt) {
                    return [pt[0], '10%'];
                }
            },
            toolbox: {
                feature: {
                    dataZoom: {
                        yAxisIndex: 'none'
                    },
                    restore: {},
                    saveAsImage: {}
                }
            },
            xAxis: {
                type: 'category',
                boundaryGap: false,
                data: datetimehist,
            },
            yAxis: {
                type: 'value',
            },
            series: [
                {
                    name: 'GDU',
                    type: 'line',
                    smooth: true,
                    symbol: 'circle',
                    symbolSize: 7,
                    sampling: 'average',
                    lineStyle: {
                        color: '#233c46',
                        width: 1,
                    },
                    itemStyle: {
                        color: '#233c46',
                    },
                    data: gduhist
                }
            ]
        };
    }

    // use configuration item and data specified to show chart
    myChart_gdu.setOption(option_gdu);

    if($('#area_chart_eto').length > 0) {

        // based on prepared DOM, initialize echarts instance
        var myChart_eto = echarts.init(document.getElementById('area_chart_eto'));

        var option_eto = {
            tooltip: {
                trigger: 'axis',
                position: function (pt) {
                    return [pt[0], '10%'];
                }
            },
            toolbox: {
                feature: {
                    dataZoom: {
                        yAxisIndex: 'none'
                    },
                    restore: {},
                    saveAsImage: {}
                }
            },
            xAxis: {
                type: 'category',
                boundaryGap: false,
                data: datetimehist,
            },
            yAxis: {
                type: 'value',
                min: 0,
                max: 1,
            },
            series: [
                {
                    name: 'ETo',
                    type: 'line',
                    smooth: true,
                    symbol: 'circle',
                    symbolSize: 7,
                    sampling: 'average',
                    lineStyle: {
                        color: '#233c46',
                        width: 1,
                    },
                    itemStyle: {
                        color: '#233c46',
                    },
                    data: etohist
                }
            ]
        };
    }

    // use configuration item and data specified to show chart
    myChart_eto.setOption(option_eto);

    if($('#area_chart_accum_eto').length > 0) {

        // based on prepared DOM, initialize echarts instance
        var myChart_accum_eto = echarts.init(document.getElementById('area_chart_accum_eto'));

        var option_accum_eto = {
            tooltip: {
                trigger: 'axis',
                position: function (pt) {
                    return [pt[0], '10%'];
                }
            },
            toolbox: {
                feature: {
                    dataZoom: {
                        yAxisIndex: 'none'
                    },
                    restore: {},
                    saveAsImage: {}
                }
            },
            xAxis: {
                type: 'category',
                boundaryGap: false,
                data: datetimehist,
            },
            yAxis: {
                type: 'value',
                // min: 0,
                // max: 'dataMax',
            },
            series: [
                {
                    name: 'AccumETo',
                    type: 'line',
                    smooth: true,
                    symbol: 'circle',
                    symbolSize: 7,
                    sampling: 'average',
                    lineStyle: {
                        color: '#233c46',
                        width: 1,
                    },
                    itemStyle: {
                        color: '#233c46',
                    },
                    data: accum_etohist,
                }
            ]
        };
    }

    // use configuration item and data specified to show chart
    myChart_accum_eto.setOption(option_accum_eto);

    if($('#area_chart_rain_1h').length > 0) {

        // based on prepared DOM, initialize echarts instance
        var myChart_rain_1h = echarts.init(document.getElementById('area_chart_rain_1h'));

        var option_rain_1h = {
            tooltip: {
                trigger: 'axis',
                position: function (pt) {
                    return [pt[0], '10%'];
                }
            },
            toolbox: {
                feature: {
                    dataZoom: {
                        yAxisIndex: 'none'
                    },
                    restore: {},
                    saveAsImage: {}
                }
            },
            xAxis: {
                type: 'category',
                boundaryGap: false,
                data: datetimehist,
            },
            yAxis: {
                type: 'value',
            },
            series: [
                {
                    name: 'Rain',
                    type: 'line',
                    smooth: true,
                    symbol: 'circle',
                    symbolSize: 7,
                    sampling: 'average',
                    lineStyle: {
                        color: '#233c46',
                        width: 1,
                    },
                    itemStyle: {
                        color: '#233c46',
                    },
                    data: rains_1hhist,
                }
            ]
        };
    }

    // use configuration item and data specified to show chart
    myChart_rain_1h.setOption(option_rain_1h);

    if($('#area_chart').length > 0) {

        // based on prepared DOM, initialize echarts instance
        var myChart = echarts.init(document.getElementById('area_chart'));

        var option = {
            tooltip: {
                trigger: 'axis',
                position: function (pt) {
                    return [pt[0], '10%'];
                }
            },
            toolbox: {
                feature: {
                    dataZoom: {
                        yAxisIndex: 'none'
                    },
                    restore: {},
                    saveAsImage: {}
                }
            },
            xAxis: {
                type: 'category',
                boundaryGap: false,
                data: datetimehist,
            },
            yAxis: {
                type: 'value',
                min: 0,
                max: 120,
            },
            series: [
                {
                    name: 'Temp',
                    type: 'line',
                    smooth: true,
                    symbol: 'circle',
                    symbolSize: 7,
                    sampling: 'average',
                    lineStyle: {
                        color: '#233c46',
                        width: 1,
                    },
                    itemStyle: {
                        color: '#233c46',
                    },
                    data: temphist
                }
            ]
        };
    }

    // use configuration item and data specified to show chart
    myChart.setOption(option);

    if($('#area_chart_2').length > 0) {

        // based on prepared DOM, initialize echarts instance
        var myChart2 = echarts.init(document.getElementById('area_chart_2'));

        var option2 = {
            tooltip: {
                trigger: 'axis',
                position: function (pt) {
                    return [pt[0], '10%'];
                }
            },
            toolbox: {
                feature: {
                    dataZoom: {
                        yAxisIndex: 'none'
                    },
                    restore: {},
                    saveAsImage: {}
                }
            },
            xAxis: {
                type: 'category',
                boundaryGap: false,
                data: datetimehist
            },
            yAxis: {
                type: 'value',
                min: 0,
                max: 50,
            },
            series: [
                {
                    name: 'Wind',
                    type: 'line',
                    smooth: true,
                    symbol: 'circle',
                    symbolSize: 7,
                    sampling: 'average',
                     lineStyle: {
                        color: '#233c46',
                        width: 1,
                    },
                    itemStyle: {
                        color: '#233c46',
                    },
                    data: windhist
                }
            ]
        };
    }

    // use configuration item and data specified to show chart
    myChart2.setOption(option2);

    if($('#area_chart_3').length > 0) {

        // based on prepared DOM, initialize echarts instance
        var myChart3 = echarts.init(document.getElementById('area_chart_3'));

        var option3 = {
            tooltip: {
                trigger: 'axis',
                position: function (pt) {
                    return [pt[0], '10%'];
                }
            },
            toolbox: {
                feature: {
                    dataZoom: {
                        yAxisIndex: 'none'
                    },
                    restore: {},
                    saveAsImage: {}
                }
            },
            xAxis: {
                type: 'category',
                boundaryGap: false,
                data: datetimehist
            },
            yAxis: {
                type: 'value',
                min: 980,
                max: 1040,
            },
            series: [
                {
                    name: 'Pressure',
                    type: 'line',
                    smooth: true,
                    symbol: 'circle',
                    symbolSize: 7,
                    sampling: 'average',
                    lineStyle: {
                        color: '#233c46',
                        width: 1,
                    },
                    itemStyle: {
                        color: '#233c46',
                    },
                    data: presshist
                }
            ]
        };
    }

    // use configuration item and data specified to show chart
    myChart3.setOption(option3);

    window.onresize = function() {
        myChart_accum_gdu.resize();
        myChart_eto.resize();
        myChart_gdu.resize();
        myChart_accum_eto.resize();
        myChart_rain_1h.resize();
        myChart.resize();
        myChart2.resize();
        myChart3.resize();
    };

});
