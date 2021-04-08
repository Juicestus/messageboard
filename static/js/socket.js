/*
 * Main Socket Manager
 * (c) Justus Languell 2020-2021
 */
	
var lastSent = 0; // The time since last sent message (UNIX timestamp)
var sendDelay = 5;	// Delay between sends


$(document).ready(function() // On page load
{
    document.getElementById('newmsg').innerHTML = `There are no new messages.`;
	scrollDown(); // Scroll down messages on document load
	var socket = io();	// Inst Socket IO connection
    newmsgs = -1;	// Set newmsg amm 

	socket.on('connect',function()	// On socket connection
	{ 
		scrollDown(); // Scroll down messagese
		socket.emit('connected') // Send out that it connected, not really used

		var form = $('form').on('submit',function(f) // On form submit
		{ 
			f.preventDefault(); // Prevent default action
			var time = (new Date).getTime();	// Get the current time as UNIX timestamp

			if (time > lastSent + (sendDelay * 1000)) // Looks to see if its been longer than the delay since last send
			{	
				var username = document.getElementById('userbox').innerHTML;	// Sets username to username box
				//var msg = document.getElementById('messageArea').value; // Sets message to message box
				var msg = document.getElementById('messageArea').innerHTML;
				var file = document.getElementById('fileUpload').files[0];

				document.getElementById('fileUpload').type = "text";
				document.getElementById('fileUpload').type = "file";

				
				var reader = new FileReader();

				reader.onloadend = function () 
				{
					src = reader.result;
					send(socket, username, msg, time, src)
				};

				if (file)
				{
					reader.readAsDataURL(file)
				}
				else
				{
					send(socket, username, msg, time, "NOIMAGE")
				};


			}
			else
			{
				var time = (new Date).getTime();
				var waittime = (lastSent + (sendDelay * 1000) - time);
				var disptime = Math.round(waittime / 1000);
				document.getElementById('waitmsg').innerHTML = `Must wait ${disptime} more seconds!`;

				setTimeout(function()
				{
					document.getElementById('waitmsg').innerHTML = '';
				}
				, waittime);
			};
		});	
	});

	// On new message input
	socket.on('newMessage', function(servedMessages, cb)
	{
		var messages = Array.from(servedMessages); // Get messages from array from server input
		var len = messages.length;	// Get the length of the list
		var firsttime = messages[0].time; // The time of the first message
		processMessages(messages);	// Call the process function, loading messages on page
		notifyMe();	// Call the notify function, telling the user if they're not active
		newmsgs++; // There is a new message so raise it by 1

		// Format the message sentance at the bottom

		if (newmsgs != 1) {var s1 = 's';} else {var s1 = '';}; 
		if (newmsgs != 1) {var a1 = 'are';} else {var a1 = 'is';}; // Format the message sentance at the bottom
		if (len != 1) {var s2 = 's';} else {var s2 = '';};
		if (len != 1) {var a2 = 'are';} else {var a2 = 'is';};

		// Load the message sentance
		document.getElementById('newmsg').innerHTML = `• ${newmsgs} new message${s1} &nbsp;	&nbsp;`; //• ${len} message${s2} since ${firsttime}`; 
		scrollDown(); // Scroll down to newest message
	});
});