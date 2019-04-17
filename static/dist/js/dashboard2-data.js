/*Dashboard2 Init*/

// Django template tag creates the json allsites object
var datetimehist = JSON.parse(document.getElementById('datetimehist').textContent);
var temphist = JSON.parse(document.getElementById('temphist').textContent);
var windhist = JSON.parse(document.getElementById('windhist').textContent);
var presshist = JSON.parse(document.getElementById('presshist').textContent);

console.log(temphist);
console.log(datetimehist);
console.log(windhist);
console.log(presshist);

"use strict"; 
$(document).ready(function() {

    if($('#area_chart').length > 0) {

        // based on prepared DOM, initialize echarts instance
        var myChart = echarts.init(document.getElementById('area_chart'));

        // specify chart configuration item and data
        var option = {
            tooltip: {
                trigger: 'item',
                formatter: '{a} <br/>{b} : {c}'
            },
            xAxis: {
                type: 'category',
                data: datetimehist,
            },
            yAxis: {
                type: 'value',
                splitLine: {
                    show: false
                },
            },
            series: [{
                color: ['#4a6b78'],
                data: temphist,
                type: 'line',
            }]
        };

    }

    // use configuration item and data specified to show chart
    myChart.setOption(option);


    if($('#area_chart_2').length > 0) {

        // based on prepared DOM, initialize echarts instance
        var myChart2 = echarts.init(document.getElementById('area_chart_2'));

        // specify chart configuration item and data
        var option2 = {
            xAxis: {
                type: 'category',
                data: datetimehist,
            },
            yAxis: {
                type: 'value',
                splitLine: {
                    show: false
                },
            },
            series: [{
                color: ['#4a6b78'],
                data: windhist,
                type: 'line',
            }]
        };

    }

    // use configuration item and data specified to show chart
    myChart2.setOption(option2);

    if($('#area_chart_3').length > 0) {

        // based on prepared DOM, initialize echarts instance
        var myChart3 = echarts.init(document.getElementById('area_chart_3'));

        // specify chart configuration item and data
        var option3 = {
            xAxis: {
                type: 'category',
                data: datetimehist,
            },
            yAxis: {
                type: 'value',
                splitLine: {
                    show: false
                },
                min:1000,
                max:1020,
            },
            series: [{
                color: ['#4a6b78'],
                data: presshist,
                type: 'line',
            }]
        };

    }

    // use configuration item and data specified to show chart
    myChart3.setOption(option3);

    window.onresize = function() {
        myChart.resize();
        myChart2.resize();
        myChart3.resize();
    };

});
