$(document).ready(function() {

  $(".datepicker").datepicker();

	$( ".timepicker" ).timepicker({
			minutes: { interval: 15 },
      showNowButton: true,
      showPeriod: true,
      defaultTime: '',
    	//showLeadingZero: true,
   		hours: {starts: 6, ends: 23},
   		rows: 3,
   		showPeriodLabels: true,
  		//minuteText: 'Min'
	});
  /*
  $( ".timepicker" ).after($('<button type="button" class="btn btn-success btn-sm btn-now">Now</button>'));
  $( ".btn-now" ).click(function() {
      var dt = new Date();
      var time = dt.getHours() + ":" + dt.getMinutes();
      $(this).prev().attr('value', /*$.now()\\*\\/time)
  });*/
});
