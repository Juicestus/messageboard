/*
 * Helper Functions
 * (c) Justus Languell 2020-2021
 */

// Scrolls to bottom
function scrollDown() 
{
	$('div.messages-cont').animate({ scrollTop: $('div.messages-cont')[0].scrollHeight}, 500);
}

// I forgot what this does and I doubt its still in use
function extractContent(s) 
{
	var span = document.createElement('span');
	span.innerHTML = s;
	return span.textContent;
};


function copyBTCAddy()
{

	addy = 'bc1q9wy07jg2kjgaw6kshfp2z84xnf3asd9f6lggkj';
	
	/*
	var elem = document.createElement("input");
	elem.setAttribute('type','text');
	elem.setAttribute('value',addy);
	*/

	var elem = document.getElementById("btcaddy");
	elem.setAttribute('type','text');

	elem.select();
	elem.setSelectionRange(0, 99999);

	console.log(elem)
	document.execCommand("copy");

	elem.setAttribute('type','hidden');


	alert('Copied BTC Address to Clipboard')
}