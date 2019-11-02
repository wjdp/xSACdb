$( document ).ready( function() {
	$('.hidden-section-actual').hide()
	$('.hidden-section-button').click(function(){
		$('i', this).toggleClass('fa-plus')
		$('i', this).toggleClass('fa-minus')
		$(this).next(".hidden-section-actual").toggle('fast');
	});

});
