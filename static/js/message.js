/*
 * Message handling functions
 * (c) Justus Languell 2020-2021
 */

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

		console.log(message.src)

		if (message.src != 'NOIMAGE')
		{
			image = `${breaks}<br><img id src='${message.src}'></img>`;
		}
		table += `<tr><td class="msgtd"><span>${message.username}</span></td><td class="msgtd"><span style='width: 575px;'>${message.msg}${image}</span></td><td class="msgtd"><span><code>${message.time}</code></span></td></tr>`
		
		scrollDown();
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
