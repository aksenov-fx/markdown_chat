<%*
  const editor = app.workspace.activeLeaf.view.sourceMode.cmEditor; 
  const noteContent = editor.getValue();
  const noteArray = noteContent.split("# ");
  
  if (noteArray.length > 1) { 
    const firstPart = noteArray[0] + "# ";
    editor.setValue(firstPart); 
      
    // Set cursor to end of the last line
    const lastLine = editor.lastLine();
    const cursorPosition = { line: lastLine, ch: editor.getLine(lastLine).length }; 
    editor.setCursor(cursorPosition);
  }
%>