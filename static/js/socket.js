/*
 * Main Socket Manager
 * (c) Justus Languell 2020-2021
 */
	
/*
 * Note to self
 * Rework the entire socket system as a class
 * or at least somthing similar to the Quill
 * handler bc its rly shitty rn
 */

/* 
 * Note to self
 * Just clean up th JavaScript in general
 * bc it's not as good as the Python
 */

/* 
 * Note to self
 * I know u want to kill yourself bc
 * of some of this. I just wanted to say
 * go for it. Just end our suffering.
 */


var lastSent = 0; // The time since last sent message (UNIX timestamp)
var sendDelay = 5;	// Delay between sends
var msgCount = 0;

$(document).ready(function() 
{

	var quill = getQuillE();
	qLimit(quill);

    document.getElementById('newmsg').innerHTML = `There are no new messages.&nbsp;&nbsp;&nbsp;&nbsp;`;
	scrollDown(); 
	var socket = io();	
    newmsgs = -1;

	// On connection, handles posting
	socket.on('connect',function()	
	{ 
		scrollDown(); 
		socket.emit('connected') 

		var form = $('form').on('submit',function(f) 
		{ 
			f.preventDefault(); 
			var time = (new Date).getTime();	

			if (time > lastSent + (sendDelay * 1000)) 
			{	
				//var username = $('input.username').val();
				var username = USER;
				var file = document.getElementById('fileUpload').files[0];

				var delta = quill.getContents();

				var parsed = parseDelta(delta);
				var msg = parsed[0];
				var embfile = parsed[1];
				var webimg = parsed[2];

				document.getElementById('fileUpload').type = "text";
				document.getElementById('fileUpload').type = "file";
								
				var reader = new FileReader();

				reader.onloadend = function() 
				{
					src = reader.result;
					send(socket, username, msg, time, src, webimg, quill);
				};

				if (file)
				{
					reader.readAsDataURL(file);
				}
				else
				{
					send(socket, username, msg, time, embfile, webimg, quill);
				};
			}
			else
			{
				var time = (new Date).getTime();
				var waittime = (lastSent + (sendDelay * 1000) - time);
				var disptime = Math.round(waittime / 1000);
				document.getElementById('waitmsg').innerHTML = `• Must wait ${disptime} more seconds!&nbsp;&nbsp;&nbsp;`;

				setTimeout(function()
				{
					document.getElementById('waitmsg').innerHTML = '';
				}
				, waittime);
			};
		});	
	});

	// On recived socket
	socket.on('newMessage', function(servedMessages, cb)
	{
		var messages = Array.from(servedMessages); 
		var len = messages.length;	
		var firsttime = messages[0].time; 
		processMessages(messages, USER);
		notifyMe();	

		if (len > msgCount)
		{
			msgCount = len;
		};

		if (msgCount != 1) {var s1 = 's';} else {var s1 = '';}; 
		if (msgCount != 1) {var a1 = 'are';} else {var a1 = 'is';}; 
		if (len != 1) {var s2 = 's';} else {var s2 = '';};
		if (len != 1) {var a2 = 'are';} else {var a2 = 'is';};

		document.getElementById('newmsg').innerHTML = `• ${msgCount} new message${s1} &nbsp;&nbsp;&nbsp;&nbsp;`; //• ${len} message${s2} since ${firsttime}`; 
		scrollDown();
	});
});
