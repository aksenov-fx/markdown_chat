<%*
const modeNames = ["Default", "Questions"];
const currentIndex = modeNames.findIndex(mode => tp.file.content.includes(`{${mode}}`));

if (currentIndex !== -1) {
    const nextIndex = (currentIndex + 1) % modeNames.length;
    const currentMode = modeNames[currentIndex];
    const nextMode = modeNames[nextIndex];
    
    const newContent = tp.file.content.replace(`{${currentMode}}`, `{${nextMode}}`);
    await app.vault.modify(tp.file.find_tfile(tp.file.title), newContent);
    new Notice(`Mode: ${nextMode}`);
}
%>