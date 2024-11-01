const { Plugin } = require('obsidian');
const net = require('net');
const path = require('path');

class MyPlugin extends Plugin {
    async onload() {

        this.addCommand({
            id: 'send-note-path',
            name: 'Send note path to Python Server',
            callback: () => {
                const activeFile = this.app.workspace.getActiveFile();
                if (activeFile) {

                    const vaultPath = this.app.vault.adapter.basePath;
                    const absolutePath = path.join(vaultPath, activeFile.path);
                    
                    this.app.commands.executeCommandById('editor:save-file')
                    this.sendCommandToServer(absolutePath);

                } else {
                    console.log('No file is currently open');
                }
            }
        });
    }

/*         this.addCommand({
            id: 'send-relative-path',
            name: 'Send Relative Path to Python Server',
            callback: () => {
                const activeFile = this.app.workspace.getActiveFile();
                if (activeFile) {
                    const relativePath = activeFile.path;
                    this.sendCommandToServer(relativePath);
                } else {
                    console.log('No file is currently open');
                }
            }
        });
 */

    sendCommandToServer(command) {
        const client = new net.Socket();
        client.connect(9999, 'localhost', () => {
            console.log('Connected to Python server');
            client.write(command);
            client.destroy(); // Kill client after sending command
        });

        client.on('data', (data) => {
            console.log('Received: ' + data);
            client.destroy(); // Kill client after server's response
        });

        client.on('close', () => {
            console.log('Connection closed');
        });

        client.on('error', (err) => {
            console.error('Connection error: ', err);
        });
    }
}

module.exports = MyPlugin;