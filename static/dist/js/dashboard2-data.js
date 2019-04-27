/*Dashboard2 Init*/

// Django template tag creates the json allsites object
var datetimehist = JSON.parse(document.getElementById('datetimehist').textContent);
var temphist = JSON.parse(document.getElementById('temphist').textContent);
var windhist = JSON.parse(document.getElementById('windhist').textContent);
var presshist = JSON.parse(document.getElementById('presshist').textContent);
var etohist = JSON.parse(document.getElementById('etohist').textContent);

console.log(temphist);
console.log(datetimehist);
console.log(windhist);
console.log(presshist);
console.log(etohist);

"use strict"; 
$(document).ready(function() {

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
            // title: {
            //     left: 'center',
            //     text: 'This is a test plot',
            // },
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
            dataZoom: [{
                type: 'inside',
                start: 0,
                end: 100
            }, {
                start: 0,
                end: 10,
                handleIcon: 'M10.7,11.9v-1.3H9.3v1.3c-4.9,0.3-8.8,4.4-8.8,9.4c0,5,3.9,9.1,8.8,9.4v1.3h1.3v-1.3c4.9-0.3,8.8-4.4,8.8-9.4C19.5,16.3,15.6,12.2,10.7,11.9z M13.3,24.4H6.7V23h6.6V24.4z M13.3,19.6H6.7v-1.4h6.6V19.6z',
                handleSize: '80%',
                handleStyle: {
                    color: '#fff',
                    shadowBlur: 3,
                    shadowColor: 'rgba(0, 0, 0, 0.6)',
                    shadowOffsetX: 2,
                    shadowOffsetY: 2
                }
            }],
            series: [
                {
                    name: 'Temp',
                    type: 'line',
                    smooth: true,
                    symbol: 'none',
                    sampling: 'average',
                    lineStyle: {
                        color: '#233c46',
                        width: 1,
                    },
                    areaStyle: {
                        color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [{
                            offset: 0.5,
                            color: '#ced8dc'
                        }, {
                            offset: 1,
                            color: '#4a6b78'
                        }])
                    },
                    data: etohist
                }
            ]
        };
    }

    // use configuration item and data specified to show chart
    myChart_eto.setOption(option_eto);

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
            // title: {
            //     left: 'center',
            //     text: 'This is a test plot',
            // },
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
            dataZoom: [{
                type: 'inside',
                start: 0,
                end: 100
            }, {
                start: 0,
                end: 10,
                handleIcon: 'M10.7,11.9v-1.3H9.3v1.3c-4.9,0.3-8.8,4.4-8.8,9.4c0,5,3.9,9.1,8.8,9.4v1.3h1.3v-1.3c4.9-0.3,8.8-4.4,8.8-9.4C19.5,16.3,15.6,12.2,10.7,11.9z M13.3,24.4H6.7V23h6.6V24.4z M13.3,19.6H6.7v-1.4h6.6V19.6z',
                handleSize: '80%',
                handleStyle: {
                    color: '#fff',
                    shadowBlur: 3,
                    shadowColor: 'rgba(0, 0, 0, 0.6)',
                    shadowOffsetX: 2,
                    shadowOffsetY: 2
                }
            }],
            series: [
                {
                    name: 'Temp',
                    type: 'line',
                    smooth: true,
                    symbol: 'none',
                    sampling: 'average',
                    lineStyle: {
                        color: '#233c46',
                        width: 1,
                    },
                    areaStyle: {
                        color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [{
                            offset: 0.5,
                            color: '#ced8dc'
                        }, {
                            offset: 1,
                            color: '#4a6b78'
                        }])
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
            // title: {
            //     left: 'center',
            //     text: 'This is a test plot',
            // },
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
            dataZoom: [{
                type: 'inside',
                start: 0,
                end: 100
            }, {
                start: 0,
                end: 10,
                handleIcon: 'M10.7,11.9v-1.3H9.3v1.3c-4.9,0.3-8.8,4.4-8.8,9.4c0,5,3.9,9.1,8.8,9.4v1.3h1.3v-1.3c4.9-0.3,8.8-4.4,8.8-9.4C19.5,16.3,15.6,12.2,10.7,11.9z M13.3,24.4H6.7V23h6.6V24.4z M13.3,19.6H6.7v-1.4h6.6V19.6z',
                handleSize: '80%',
                handleStyle: {
                    color: '#fff',
                    shadowBlur: 3,
                    shadowColor: 'rgba(0, 0, 0, 0.6)',
                    shadowOffsetX: 2,
                    shadowOffsetY: 2
                }
            }],
            series: [
                {
                    name: 'Wind',
                    type: 'line',
                    smooth: true,
                    symbol: 'none',
                    sampling: 'average',
                     lineStyle: {
                        color: '#233c46',
                        width: 1,
                    },
                    areaStyle: {
                        color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [{
                            offset: 0.5,
                            color: '#ced8dc'
                        }, {
                            offset: 1,
                            color: '#4a6b78'
                        }])
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
            // title: {
            //     left: 'center',
            //     text: 'This is a test plot',
            // },
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
            dataZoom: [{
                type: 'inside',
                start: 0,
                end: 100
            }, {
                start: 0,
                end: 10,
                handleIcon: 'M10.7,11.9v-1.3H9.3v1.3c-4.9,0.3-8.8,4.4-8.8,9.4c0,5,3.9,9.1,8.8,9.4v1.3h1.3v-1.3c4.9-0.3,8.8-4.4,8.8-9.4C19.5,16.3,15.6,12.2,10.7,11.9z M13.3,24.4H6.7V23h6.6V24.4z M13.3,19.6H6.7v-1.4h6.6V19.6z',
                handleSize: '80%',
                handleStyle: {
                    color: '#fff',
                    shadowBlur: 3,
                    shadowColor: 'rgba(0, 0, 0, 0.6)',
                    shadowOffsetX: 2,
                    shadowOffsetY: 2
                }
            }],
            series: [
                {
                    name: 'Pressure',
                    type: 'line',
                    smooth: true,
                    symbol: 'none',
                    sampling: 'average',
                    lineStyle: {
                        color: '#233c46',
                        width: 1,
                    },
                    areaStyle: {
                        color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [{
                            offset: 0.5,
                            color: '#ced8dc'
                        }, {
                            offset: 1,
                            color: '#4a6b78'
                        }])
                    },
                    data: presshist
                }
            ]
        };
    }

    // use configuration item and data specified to show chart
    myChart3.setOption(option3);

    window.onresize = function() {
        myChart_eto.resize();
        myChart.resize();
        myChart2.resize();
        myChart3.resize();
    };

});
