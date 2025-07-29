const { Plugin, Notice } = require('obsidian');
const net = require('net');
const path = require('path');

class MyPlugin extends Plugin {
    async onload() {
        
        this.addCommand({
            id: 'chat',
            name: 'Chat',
            hotkeys: [{ modifiers: ['Alt'], key: 'S' }],
            callback: () => {
                new Notice(`Chat`);
                this.sendNoteCommand('chat');
            }
        });

        this.addCommand({
            id: 'remove-last-response',
            name: 'Remove Last Response',
            hotkeys: [{ modifiers: ['Alt'], key: 'Z' }],
            callback: () => {
                new Notice(`Remove Last Response`);
                this.sendNoteCommand('remove_last_response');
            }
        });

        this.addCommand({
            id: 'interrupt-write',
            name: 'Interrupt Write',
            hotkeys: [{ modifiers: ['Alt'], key: 'Q' }],
            callback: () => {
                new Notice(`Interrupt Write`);
                this.sendNoteCommand('interrupt_write');
            }
        });

        this.addCommand({
            id: 'set-model-1',
            name: 'Set model 1',
            hotkeys: [{ modifiers: ['Alt'], key: '1' }],
            callback: async () => {
                new Notice(`Set model 1`);
                await this.setModelNumber(1);
                this.sendNoteCommand('set_model', 1);
            }
        });

        this.addCommand({
            id: 'set-model-2',
            name: 'Set model 2',
            hotkeys: [{ modifiers: ['Alt'], key: '2' }],
            callback: async () => {
                new Notice(`Set model 2`);
                await this.setModelNumber(2);
                this.sendNoteCommand('set_model', 2);
            }
        });

        this.addCommand({
            id: 'set-model-3',
            name: 'Set model 3',
            hotkeys: [{ modifiers: ['Alt'], key: '3' }],
            callback: async () => {
                new Notice(`Set model 3`);
                await this.setModelNumber(3);
                this.sendNoteCommand('set_model', 3);
            }
        });

        this.addCommand({
            id: 'set-model-4',
            name: 'Set model 4',
            hotkeys: [{ modifiers: ['Alt'], key: '4' }],
            callback: async () => {
                new Notice(`Set model 4`);
                await this.setModelNumber(4);
                this.sendNoteCommand('set_model', 4);
            }
        });

        this.addCommand({
            id: 'set-model-5',
            name: 'Set model 5',
            hotkeys: [{ modifiers: ['Alt'], key: '5' }],
            callback: async () => {
                new Notice(`Set model 5`);
                await this.setModelNumber(5);
                this.sendNoteCommand('set_model', 5);
            }
        });

        this.addCommand({
            id: 'enable-debug',
            name: 'Enable Debug Mode',
            callback: () => {
                new Notice(`Enable Debug Mode`);
                this.sendNoteCommand('enable_debug');
            }
        });

        this.addCommand({
            id: 'disable-debug',
            name: 'Disable Debug Mode',
            callback: () => {
                new Notice(`Disable Debug Mode`);
                this.sendNoteCommand('disable_debug');
            }
        });
    }

    async setModelNumber(modelInt) {
        const activeFile = this.app.workspace.getActiveFile();
        if (!activeFile) {
            new Notice('No active file');
            return;
        }

        await this.app.fileManager.processFrontMatter(activeFile, (frontmatter) => {
            frontmatter.model_number = modelInt;
        });

        new Notice(`Model number updated to: ${modelInt}`);
    }

    getNotePath() {
        const activeFile = this.app.workspace.getActiveFile();
        if (activeFile) {
            const vaultPath = this.app.vault.adapter.basePath;
            const absolutePath = path.join(vaultPath, activeFile.path);

            const folderPath = activeFile.parent?.path || '';
            const absoluteFolderPath = path.join(vaultPath, folderPath);

            return absolutePath;

        } else {
            console.log('No file is currently open');
        }
    }

    sendNoteCommand(methodName, model_number = 0) {
        this.app.commands.executeCommandById('editor:save-file');

        var absolutePath = this.getNotePath();
        var parameters = `${absolutePath},${methodName}`;

        this.sendCommandToServer(parameters);
    }

    sendCommandToServer(command) {
        const client = new net.Socket();
        client.connect(9992, 'localhost', () => {
            console.log('Connected to Python server');
            client.write(command);
            client.destroy();
        });

        client.on('data', (data) => {
            console.log('Received: ' + data);
            client.destroy();
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