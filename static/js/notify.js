/*
 * Notification Manager
 * (c) Justus Languell 2021
 */

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