<%* 
	// Execute the first command
	app.commands.executeCommandById('editor:fold-all');
	
	// Execute the second command
	//app.commands.executeCommandById('chatgpt-md:call-chatgpt-api');
	app.commands.executeCommandById('markdown-chat:send-note-path');

	// Get command ids in console:
	// Object.keys(app.commands.commands).forEach(command => console.log(command));
%>