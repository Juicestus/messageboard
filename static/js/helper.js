/*
 * Helper Functions
 * (c) Justus Languell 2020-2021
 */

// Scrolls to bottom
function scrollDown() 
{
	$('table')[3].scrollTop = $('table')[3].scrollHeight; 
};

// I forgot what this does and I doubt its still in use
function extractContent(s) 
{
	var span = document.createElement('span');
	span.innerHTML = s;
	return span.textContent;
};

	  