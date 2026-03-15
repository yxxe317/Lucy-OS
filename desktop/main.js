const { app, BrowserWindow, Tray, Menu, globalShortcut, ipcMain, Notification } = require('electron')
const path = require('path')
const Store = require('electron-store')

const store = new Store()
let mainWindow = null
let tray = null
let isQuitting = false

const BACKEND_URL = 'http://127.0.0.1:8000'

function createWindow() {
  mainWindow = new BrowserWindow({
    width: 1400,
    height: 900,
    minWidth: 800,
    minHeight: 600,
    webPreferences: {
      nodeIntegration: false,
      contextIsolation: true,
      preload: path.join(__dirname, 'preload.js')
    },
    backgroundColor: '#0a0a0a'
  })

  // Load frontend from Vite dev server
  mainWindow.loadURL('http://localhost:5173')
  
  mainWindow.on('close', (e) => {
    if (!isQuitting && store.get('minimizeToTray', true)) {
      e.preventDefault()
      mainWindow.hide()
    }
  })
}

function createTray() {
  const iconPath = path.join(__dirname, 'icon.png')
  tray = new Tray(iconPath)
  
  const contextMenu = Menu.buildFromTemplate([
    { label: 'Show Lucy OS', click: () => mainWindow.show() },
    { label: 'Hide to Tray', click: () => mainWindow.hide() },
    { type: 'separator' },
    { label: 'Quit', click: () => { isQuitting = true; app.quit() } }
  ])
  
  tray.setToolTip('Lucy OS v17.0')
  tray.setContextMenu(contextMenu)
  tray.on('double-click', () => mainWindow.show())
}

function registerHotkey() {
  globalShortcut.register('CommandOrControl+Shift+L', () => {
    mainWindow.isVisible() ? mainWindow.hide() : mainWindow.show()
  })
}

app.whenReady().then(() => {
  createWindow()
  createTray()
  registerHotkey()
})

ipcMain.handle('send-notification', (event, { title, body }) => {
  new Notification({ title, body }).show()
})

ipcMain.handle('minimize-to-tray', () => mainWindow.hide())