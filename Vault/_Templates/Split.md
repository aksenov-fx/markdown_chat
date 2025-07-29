<%*
const editor = app.workspace.activeLeaf.view.editor
const cursor = editor.getCursor()
const content = editor.getValue().slice(editor.posToOffset(cursor))

const searchText = '\n----\n'
const replaceText = '\n----\n****\n'

const index = content.indexOf(searchText)

if (index !== -1) {
    const absolutePosition = editor.posToOffset(cursor) + index
    
    const from = editor.offsetToPos(absolutePosition)
    const to = editor.offsetToPos(absolutePosition + searchText.length)
    
    editor.replaceRange(replaceText, from, to)
}
%>