$(document).ready(function(){
	setup();
});

function setup() {
	markActiveLinks();
	setup_did_finish();
}


/**
 * Adds the class '.active' to all <a> elements which
 * are children of a <nav> element and have and href 
 * attribute that is equal to the current url.
 */
function markActiveLinks() {
	const loc = window.location.pathname;

	$('nav').find('a').each(function() {
	  $(this).toggleClass('active', $(this).attr('href') == loc);
   });
}

/**
 * Removes the '.cloak' class from all elements that have it.
 */
function setup_did_finish() {
	$('.cloak').removeClass('cloak');
}
