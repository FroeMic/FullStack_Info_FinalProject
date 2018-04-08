let state = {
	moods: []
}

let config = {
	landingPage: {
		numberOfMoodsToShowInExploreView: 5
	}
}

$(document).ready(function(){
	setup();
	setup_did_finish();
});

function setup() {
	markActiveLinks();
	setupLandingPage();
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

function loadMoods() {
	return $.get('/api/v1/moods', function(response) {
		if (response && response.success) {
			state.moods = response.data;
		} else {
			console.log(response.error);
		}
	});
}

/**
 * Sets up the state and view for the landing page.
 */
function setupLandingPage() {
	// only invoke this function, if we are on the landing page
	if (!$('#landing-page')) {
		return;
	}

	loadMoods().then(function() {
		console.log('loaded modds', state.moods)
		addExploreMoodsView();
	});
}

function addExploreMoodsView() {
	const n = config.landingPage.numberOfMoodsToShowInExploreView;
	const moods = getRandom(state.moods, n);

	let html = ['<h4>Explore Moods</h4>']
	for (let mood of moods) {
		html.push([
			'<a href="" class="btn mood-btn">',
				mood,
			'</a>'
		].join(''))
	}

	$('#exploreMoodsContainer').empty()
	$('#exploreMoodsContainer').append(html.join(''));
}

/**
 * Returns n random elements from an array.
 * 
 * If the array has less then n elements, all elements 
 * of the array are returned.
 * @param {Array} arr 
 * @param {Number} n 
 */
function getRandom(arr, n) {
    var result = new Array(n),
        len = arr.length,
        taken = new Array(len);
    if (n > len)
        return arr;
    while (n--) {
        var x = Math.floor(Math.random() * len);
        result[n] = arr[x in taken ? taken[x] : x];
        taken[x] = --len in taken ? taken[len] : len;
    }
    return result;
}