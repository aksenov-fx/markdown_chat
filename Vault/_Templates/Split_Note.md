<%*
const editor = app.workspace.activeLeaf.view.editor;
const cursor = editor.getCursor();

// Get current file details
const currentFile = app.workspace.getActiveFile();
const currentFileName = currentFile.basename;
const currentFilePath = currentFile.path;
const currentFileFolder = currentFilePath.substring(0, currentFilePath.lastIndexOf("/"));

// Define split note details
const splitNoteName = currentFileName + " (split)";
const splitNotePath = currentFileFolder + "/" + splitNoteName + ".md";

// Check if split note exists
const splitNoteFile = app.vault.getAbstractFileByPath(splitNotePath);

if (splitNoteFile) {
    // Save cursor position
    const cursorPosition = editor.getCursor();
    
    // Merge the split note back into the current note
    const splitNoteContent = await app.vault.read(splitNoteFile);
    const currentContent = await app.vault.read(currentFile);
    
    // Append split note content
    await app.vault.modify(currentFile, currentContent + splitNoteContent);
    
    // Delete the split note
    await app.vault.delete(splitNoteFile);
    
    // Restore cursor position after the editor refreshes
    setTimeout(() => {
        editor.setCursor(cursorPosition);
    }, 10);
} else {
    // Save cursor position
    const cursorPosition = editor.getCursor();
    
    // Split the current note at cursor position
    const fullContent = editor.getValue();
    const contentBeforeCursor = fullContent.slice(0, editor.posToOffset(cursor));
    const contentAfterCursor = fullContent.slice(editor.posToOffset(cursor));
    
    // Update current note with content before cursor
    await app.vault.modify(currentFile, contentBeforeCursor);
    
    // Create new split note with content after cursor
    await app.vault.create(splitNotePath, contentAfterCursor);
    
    // Restore cursor position after the editor refreshes
    setTimeout(() => {
        editor.setCursor(cursorPosition);
    }, 10);
}
-%>