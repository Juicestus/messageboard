/*
 * Helper Functions
 * (c) Justus Languell 2020-2021
 */

function scrollDown() // Scrolls down messages
{
	$('table')[3].scrollTop = $('table')[3].scrollHeight; // Gets element using JQuery and sets scroll to bottom
};

function extractContent(s) 
{
	var span = document.createElement('span');
	span.innerHTML = s;
	return span.textContent || span.innerText;
};
	  