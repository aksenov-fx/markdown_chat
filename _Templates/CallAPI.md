<%* 
	let params = tp.frontmatter;
	if (params && params.fold === true) {
	    app.commands.executeCommandById('editor:fold-all');
	}
	
	app.commands.executeCommandById('markdown-chat:send-note-path');

	// Get command ids in console:
	// Object.keys(app.commands.commands).forEach(command => console.log(command));
%>