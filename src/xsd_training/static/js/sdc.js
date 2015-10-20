$( ".sdc-register-interest" ).click(function() {
	var csrftoken = $.cookie('csrftoken');
	var sdc_id=$( this ).data('sdc-id');

    $.ajaxSetup({
        crossDomain: false, // obviates need for sameOrigin test
        beforeSend: function(xhr, settings) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    });

	$.ajax({
		type: "POST",
		url: "reg-interest/",
		data: { sdc_id: sdc_id, action:"add" }
	}).done(function( msg ) {
	   $(".sdc-register-interest-false-"+sdc_id).hide()
       $(".sdc-register-interest-true-"+sdc_id).show()
});
});

$( ".sdc-cancel-interest" ).click(function() {
    var csrftoken = $.cookie('csrftoken');
    var sdc_id=$( this ).data('sdc-id');

    $.ajaxSetup({
        crossDomain: false, // obviates need for sameOrigin test
        beforeSend: function(xhr, settings) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    });

    $.ajax({
        type: "POST",
        url: "reg-interest/",
        data: { sdc_id: sdc_id, action:"remove" }
    }).done(function( msg ) {
       $(".sdc-register-interest-false-"+sdc_id).show()
       $(".sdc-register-interest-true-"+sdc_id).hide()
});
});

$('.popover-button').popover()

// $('.popover-button').click(function() {
//     $(this).popover('toggle')
// });