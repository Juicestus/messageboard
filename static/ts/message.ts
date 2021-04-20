/*
 * Message handling functions
 * (c) Justus Languell 2020-2021
 */

/*
 * Note to self
 * Rework the entire socket system as a class
 * or at least somthing similar to the Quill
 * handler bc its rly shitty rn
 */

function setElemIn(s ,id, t)
{
	setTimeout(() => 
		{  
			document.getElementById(id).innerHTML = s; 
		},
	t);
};

// Renders messages from list on document
function processMessages(messages, username) 
{	
	var block = '';

	for (var message of messages) 
	{
		var image = '';

		var breaks = '';
		if (!message.msg.replace(/\s/g, '').length) 
		{
			breaks = '';
		};


		if (message.webimg != 'NOIMAGE')
		{
			image = `<img id src='${message.webimg}'></img>`;
		};

		if (message.src != 'NOIMAGE')
		{
			image = `<img id src='${message.src}'></img>`;
		};


		var h = '';

		if (username != 'Guest')
		{
			if (message.msg.includes('@'+username) ||
				message.msg.includes('@all'))
			{
				h = 'highlight';
			};
		};
		
		var usrc = 'msg';
		var ver = '';
		if (message.username[message.username.length-1] == '✔')
		{
			usrc = 'verf';
		};
		  
		block += `<div class="msg-cont ${h}">`;

		block += `<div class="msg-item"><p class="${usrc}" >${message.username} ${ver}</p></div>`;
		block += `<div class="msg-item"><p class="msg">${message.msg}${image}</p></div>`;
		block += `<div class="msg-item"><p class="msg">${message.time}</p></div>`;
		block += '</div>';


		scrollDown();
	};
	
	document.getElementById('messages').innerHTML = block; 
};

// Sends socket to server
function send(socket, username, msg, time, src, webimg, q) 
{
	if (!msg.replace(/\s/g, '').length && src == "NOIMAGE" && webimg == "NOIMAGE") 
	{ 
		alert('Message does not contain any characters worth sending!');	
	} 
	else 
	{
		if (!username.replace(/\s/g, '').length) 
		{	
			alert('Must provide username!')		
		} 
		else 
		{
			socket.emit('updateMessage',
			{	
				username: username,
				msg: msg,
				time: time,
				src: src,
				webimg: webimg
			});

			document.getElementById('sendInfo').innerHTML = `Sending Message ...`; 
			setElemIn('Screening Message ...', 'sendInfo', 300);
			lastSent = time;	

			socket.on('msgNotToxic', function()
			{
				document.getElementById('sendInfo').innerHTML = `Message Sent!`; 

				setElemIn('', 'sendInfo', 2000);
			});

			socket.on('msgToxic', function()
			{
				document.getElementById('sendInfo').innerHTML = `Message Flagged for Toxicity!`; 

				setElemIn('', 'sendInfo', 2000);
			});

            qClear(q);
		};
	};
};