/* Daterange Init*/
var selectstartdate = JSON.parse(document.getElementById('selectstartdate').textContent);
var selectenddate = JSON.parse(document.getElementById('selectenddate').textContent);
var picker_start_date;
var picker_end_date;

console.log(selectstartdate);
console.log(selectenddate);

if (selectstartdate == null) {
	picker_start_date = moment().subtract(10, 'day').format('MM/DD/YYYY');
} else {
	picker_start_date = selectstartdate;
}

if (selectenddate == null) {
	picker_end_date = moment().add(1, 'day').format('MM/DD/YYYY');
} else {
	picker_end_date = selectenddate;
}

console.log('hi will');
console.log(picker_start_date);

$(function() {
  "use strict";

	/* Single table*/
	$('input[name="selectstartdate"]').daterangepicker({
		singleDatePicker: true,
		showDropdowns: true,
		minDate: '04/4/2019',
		maxDate: moment().subtract(1, 'day').format('MM/DD/YYYY'),
		startDate: picker_start_date,
		"cancelClass": "btn-secondary",
		maxYear: parseInt(moment().format('YYYY'),10)
	});

	$('input[name="selectenddate"]').daterangepicker({
		singleDatePicker: true,
		showDropdowns: true,
		minDate: '04/5/2019',
		maxDate: moment().add(1, 'day').format('MM/DD/YYYY'),
		startDate: picker_end_date,
		"cancelClass": "btn-secondary",
		maxYear: parseInt(moment().format('YYYY'),10)
	});

});
