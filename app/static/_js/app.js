let state = {
	moods: [],
	query: '',
	selectedMood: null	
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


// ========================
// ===  LANDING PAGE
// ========================

/**
 * Sets up the state and view for the landing page.
 */
function setupLandingPage() {
	// only invoke this function, if we are on the landing page
	if (!$('#landing-page')) {
		return;
	}

	loadMoods().then(function() {
		const exampleMood = getRandom(state.moods, 1)[0];
		if (exampleMood) {
			$('#input-search').attr('placeholder', 'Try "' + exampleMood + '"');
		}
		addExploreMoodsView();
	});

	$('#input-search').on('keyup', updateDropdownView); 
	$('#input-search-button').on('click', performQuery); 

	$('#exploreMoodsContainer').on('click', '.mood-btn', moodButtonClicked);

	// setup autocomplete suggestion view
	$('#autoCompleteContainer').on('mouseleave', '.autocomplete-suggestion', function (){
		$('.autocomplete-suggestion.selected').removeClass('selected');
	});

	$('#autoCompleteContainer').on('mouseenter', '.autocomplete-suggestion', function (){
		$('.autocomplete-suggestion.selected').removeClass('selected');
		$(this).addClass('selected');
	});

	$('#autoCompleteContainer').on('mousedown click', '.autocomplete-suggestion', function (e){
		var item = $(this), v = item.attr('value');
		if (v || item.hasClass('autocomplete-suggestion')) { // else outside click
			state.selectedMood = v;
			$('#input-search').val(v);
			$('.autocomplete-suggestion.selected').removeClass('selected');
			$(this).addClass('selected');
			hideDropdown();
			performQuery();
		}
		return false;
	});

	$('#searchInputDropDown').on('keydown.autocomplete', function (e){
		if (e.key == 'ArrowUp' || e.key == 'ArrowDown') {
			e.preventDefault();

			let current = $('#searchInputDropDownMenu .autocomplete-suggestion.selected').first();

			if (!current.length) {
				current = $('#searchInputDropDownMenu .autocomplete-suggestion').first();
			}

			if (!current.length) {
				// no suggestions available
				return;
			}

			let next = null;
			if (e.key == 'ArrowDown')  {
				next = current.next();
			} 
			if (e.key == 'ArrowUp') {
				next = current.prev();
			}

			if (!next.length) {
				// beginning or end of suggestions
				return;
			}

			$('#searchInputDropDownMenu .autocomplete-suggestion.selected').removeClass('selected');
			next.addClass('selected');
		}
		
		if (e.key == 'Enter' || e.key == 'Tab') {
			let current = $('#searchInputDropDownMenu .autocomplete-suggestion.selected').first();

			if (!current.length) {
				current = $('#searchInputDropDownMenu .autocomplete-suggestion').first();
			}

			if (current.length) {
				const v = current.attr('value');
				state.query = v;
				state.selectedMood = v;
				$('#input-search').val(v);
			}

			if (e.key == 'Tab') {
				e.preventDefault();
			}
			if (e.key == 'Enter') {
				performQuery();
			}

			hideDropdown();
		}

	});
}

/**
 * Adds suggestions for different moods to dropdown.
 */
function addExploreMoodsView() {
	const n = config.landingPage.numberOfMoodsToShowInExploreView;
	const moods = getRandom(state.moods, n);

	let html = ['<h4>Explore Moods</h4>']
	for (let mood of moods) {
		html.push([
			'<a href="#" class="btn mood-btn" value="', mood.toLowerCase(),'">',
				mood,
			'</a>'
		].join(''))
	}

	$('#exploreMoodsContainer').empty()
	$('#exploreMoodsContainer').append(html.join(''));
}

function moodButtonClicked(e) {
	e.preventDefault();
	const v = $(this).attr('value');
	state.query = v;
	state.selectedMood = v;
	$('#input-search').val(v);
	performQuery();

}

/**
 * Performs a query with the entered parameters.
 */
function performQuery() {
	console.log('TODO: performQuery')
	if (!state.selectedMood) {
		window.location.reload();
		return;
	} else {
		let selectedMood = $('#input-search').val() ? $('#input-search').val() : state.selectedMood;
		window.location = '/search?' + encodeQueryData({
			'mood': selectedMood
		});
	}
}

/**
 * Updates the dropdown view on the landing page.
 */
function updateDropdownView() {
	const query = $('#input-search').val();

	if (state.query === query) {
		// only update, if something changed
		return;
	} else {
		showDropdown();
		state.query = query;
	}
	
	if (!!state.query) {
		updateAutocompleteSuggestionView();
		$('#exploreMoodsContainer').addClass('hidden');
		$('#autoCompleteContainer').removeClass('hidden');
	} else {
		$('#exploreMoodsContainer').removeClass('hidden');
		$('#autoCompleteContainer').addClass('hidden');
	}
}

/**
 * Updates the autocomplete suggestions.
 */
function updateAutocompleteSuggestionView() {
	const query = $('#input-search').val().toLowerCase();
	const choices = state.moods;

	let matches = [];
	for (let choice of choices) {
		if (~choice.toLowerCase().indexOf(query)){
			matches.push(choice);
		} 
	}

	// select first mood by default
	if (!state.selectedMood && matches[0]) {
		state.selectedMood = matches[0];
	}

	let html = []
	for (let match of matches) {
		html.push([
			'<div class="autocomplete-suggestion ', (match == state.selectedMood ? 'selected' : '') ,'" value="', match, '">',
				match,
			'</div>'
		].join(''))
	}
	
	$('#autoCompleteContainer').empty()
	$('#autoCompleteContainer').append(html.join(''));
}

/**
 * Hides the dropdown on the landing page.
 */
function hideDropdown() {
	$('#searchInputDropDown').removeClass('show');
	$('#searchInputDropDownMenu').removeClass('show');
	$('#searchInputDropDown').parent().removeClass('show');
}

/**
 * Shows the dropdown on the landing page.
 */
function showDropdown() {
	$('#searchInputDropDown').addClass('show');
	$('#searchInputDropDownMenu').addClass('show');
	$('#searchInputDropDown').parent().addClass('show');
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

/**
 * Encodes a dictionary with {'key': 'value'} pairs of 
 * type string into a query string for url parameters.
 */
function encodeQueryData(data) {
	let ret = [];
	for (let d in data)
	  ret.push(encodeURIComponent(d) + '=' + encodeURIComponent(data[d]));
	return ret.join('&');
 }