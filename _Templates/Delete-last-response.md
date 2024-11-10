<%*
	const editor = app.workspace.activeLeaf.view.sourceMode.cmEditor; 
	const noteContent = editor.getValue();
	const lastIndex = noteContent.lastIndexOf('\n\n<hr class="__AI_plugin_role-assistant">');
	
	if (lastIndex !== -1) { 
	  const firstPart = noteContent.substring(0, lastIndex);
	  editor.setValue(firstPart); 
	
	  // Set cursor to end of the last line
	  const lastLine = editor.lastLine();
	  const cursorPosition = { line: lastLine, ch: editor.getLine(lastLine).length }; 
	  editor.setCursor(cursorPosition);
	}
%>