/*
 * Helper Functions
 * (c) Justus Languell 2020-2021
 */

console.log('Helper Loaded')

// Scrolls to bottom
function scrollDown() 
{
	$('div.messages-cont')[0].scrollTop = $('div.messages-cont')[0].scrollHeight; 
};

// I forgot what this does and I doubt its still in use
function extractContent(s) 
{
	var span = document.createElement('span');
	span.innerHTML = s;
	return span.textContent;
};

	  