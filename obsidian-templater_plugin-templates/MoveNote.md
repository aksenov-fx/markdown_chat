<%*
const currentNote = tp.file.find_tfile(tp.file.title);

if (!currentNote) {
    throw new Error("No active note found.");
}

// Define the path where the note should be copied
const archivePath = `_Chat/_Archive`;

// Get current datetime
const currentDate = new Date();
const timestamp = String(currentDate.getFullYear()).slice(-2) +
                  String(currentDate.getMonth()+1).padStart(2, '0') +
                  String(currentDate.getDate()).padStart(2, '0') +
                  String(currentDate.getHours()).padStart(2, '0') +
                  String(currentDate.getMinutes()).padStart(2, '0') +
                  String(currentDate.getSeconds()).padStart(2, '0');

// Create a new name for the copied note
const newName = `${timestamp}-${currentNote.basename}`;

// Define the full path for the new note
const newFilePath = `${archivePath}/${newName}.md`;

// Read the content of the current note
const content = await app.vault.read(currentNote);

// Copy the note to the new location
await app.vault.create(newFilePath, content);

// Clear Note
await tp.file.include('[[ClearNote]]')
%>