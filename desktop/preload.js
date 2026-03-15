const { contextBridge, ipcRenderer } = require('electron')

contextBridge.exposeInMainWorld('electronAPI', {
  sendNotification: (title, body) => ipcRenderer.invoke('send-notification', { title, body }),
  minimizeToTray: () => ipcRenderer.invoke('minimize-to-tray'),
  platform: process.platform
})