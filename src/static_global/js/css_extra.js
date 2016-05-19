$( document ).ready( function() {

	h = $('.row').height()

	$('.section-nav').css({'height':h+'px'})

	var store = {}

	function fetch_lesson_data(trainee,qualification,lesson) {
		if (store[trainee+'-'+qualification] == undefined) {
			$.getJSON("/training/pl-mouseover-api/?t="+trainee+"&q="+qualification, function (data){
				store[trainee+'-'+qualification]=data
				display_lesson_data(data[lesson])
			});
		}
		else {
			display_lesson_data(store[trainee+'-'+qualification][lesson])
		}
	}

	function display_lesson_data(lesson_data) {
		if ("pl" in lesson_data) {
			$('#mouse_iframe .js-lesson').html(lesson_data['code'] + " - " + lesson_data['title'])
			$('#mouse_iframe .js-uid').html(lesson_data['pl']['uid'])
			$('#mouse_iframe .js-date').html(lesson_data['pl']['date'])
			$('#mouse_iframe .js-session').html(lesson_data['pl']['session'])
			$('#mouse_iframe .js-instructor').html(lesson_data['pl']['instructor'])
			$('#mouse_iframe .js-public').html(lesson_data['pl']['public_notes'])
			$('#mouse_iframe .js-private').html(lesson_data['pl']['private_notes'])
			$('#mouse_iframe #js-banner').attr('class', lesson_data['state'])
			$('#mouse_iframe').css({'display':'block'});
		}
	}

	$('.ljs').hover(function(elem){
		var l = elem.currentTarget.dataset['l']
		var t = elem.currentTarget.dataset['t']
		var q = elem.currentTarget.dataset['q']
		fetch_lesson_data(t,q,l)
	},function(){
		$('#mouse_iframe').css({'display':'none'});
	});

	// $(document).mousemove(function(e){

 //     $('#mouse_iframe').css({'top':e.pageY+16, 'left':e.pageX-150});
 //  });

	$('.hidden-section-actual').hide()
	$('.hidden-section-button').click(function(){
		$('i', this).toggleClass('fa-plus')
		$('i', this).toggleClass('fa-minus')
		$(this).next(".hidden-section-actual").toggle('fast');
	});

});
