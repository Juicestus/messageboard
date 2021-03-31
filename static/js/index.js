/*
 * 2021 CSP Create Project
 * A realtime internet chat room using WebSockets handled with Flask SocketIO
 * Built on a Flask Python server with a JavaScript client
 */
	
var lastSent = 0; // The time since last sent message (UNIX timestamp)
var sendDelay = 5;	// Delay between sends

function scrollDown() // Scrolls down messages
{
	$('table')[3].scrollTop = $('table')[3].scrollHeight; // Gets element using JQuery and sets scroll to bottom
};

function notifyMe() // Notifies of new messag
{	
	if (Notification.permission !== 'granted') // If it doesn't have permisions
	{
		Notification.requestPermission();	// Ask for them
	} 
	else // If it does
	{	
		if (document.hidden) // If the document isn't being viewed (in other tab or window)
		{	
			var notification = new Notification('New Message');	// Notify of new message
			notification.onclick = function() // If clicked
			{		
				window.open(window.location.href);	// Brings to this page
			};
		};
	};
};

function processMessages(messages) // Loads the messages in the table
{	
	// Inst HTML for table
	var table = '';

	for (var message of messages) // For each message in messages
	{
		// Adds HTML for each message
		var image = '';

		var breaks = '<br><br>';
		var braeks = '';
		if (!message.msg.replace(/\s/g, '').length) 
		{
			breaks = '';
		}

		if (message.src != 'NOIMAGE')
		{
			image = `${breaks}<br><img src="${message.src}"></img>`;
		}
		table += `<tr><td class="msgtd"><span>${message.username}</span></td><td class="msgtd"><span style='width: 575px;'>${message.msg}${image}</span></td><td class="msgtd"><span><code>${message.time}</code></span></td></tr>`

	};
	table += '</table>'; // Closes table
	document.getElementById('messages').innerHTML = table; // Sets table in document
};

function send(socket, username, msg, time, src) 
{
	if (!msg.replace(/\s/g, '').length && src == "NOIMAGE") // Check if there are all spaces etc.
	{ 
		alert('Message does not contain any characters worth sending!');	// Alert this to the user
	} 
	else 
	{
		if (!username.replace(/\s/g, '').length) // Do the same for username
		{	
			alert('Must provide username!')		// Alert that they need a username, maybe ill remove this and if null just replace with "Anonymous"
		} 
		else 
		{
			socket.emit('updateMessage',{	
				username: username,
				msg: msg,
				time: time,
				src: src
			});

			lastSent = time;	// Update last sent
			$('#msbox').val('');
			$('input.message').val('').focus(); 	
			var msg = document.getElementById('messageArea').value = '';
		};
	};
};

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
				var username = $('input.username').val();	// Sets username to username box
				var msg = document.getElementById('messageArea').value; // Sets message to message box
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
		document.getElementById('newmsg').innerHTML = `• ${newmsgs} new message${s1} &nbsp;	&nbsp;• ${len} message${s2} since ${firsttime}`; 
		scrollDown(); // Scroll down to newest message
	});
});