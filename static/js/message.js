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

// Renders messages from list on document
function processMessages(messages) 
{	
	var table = '';

	for (var message of messages) 
	{
		var image = '';

		var breaks = '';
		if (!message.msg.replace(/\s/g, '').length) 
		{
			breaks = '';
		};

		console.log(message.src)

		if (message.webimg != 'NOIMAGE')
		{
			image = `<img id src='${message.webimg}'></img>`;
		};

		if (message.src != 'NOIMAGE')
		{
			image = `<img id src='${message.src}'></img>`;
		};
		
		table += `<tr><td class="msgtd"><span>${message.username}</span></td><td class="msgtd"><span style='width: 575px;'>${message.msg}${image}</span></td><td class="msgtd"><span><code>${message.time}</code></span></td></tr>`
		
		scrollDown();
	};
	table += '</table>'; 
	document.getElementById('messages').innerHTML = table; 
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

			lastSent = time;	
            qClear(q);
		};
	};
};
