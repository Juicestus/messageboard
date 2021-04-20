/*
 * Notification Manager
 * (c) Justus Languell 2021
 */

/* 
 * IDK if ill even use this bc
 * it's so balls. Maybe ill fix it.
 * I prob wont.
 */

// Handles Noties
function notifyMe() 
{	
	if (Notification.permission !== 'granted') 
	{
		Notification.requestPermission();	
	} 
	else // If it does
	{	
		if (document.hidden) 
		{	
			var notification = new Notification('New Message');	
			notification.onclick = function() 
			{		
				window.open(window.location.href);
			};
		};
	};
};