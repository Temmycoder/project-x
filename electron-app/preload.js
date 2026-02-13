/**
 * Electron Preload Script
 * Safe IPC bridge between renderer and main process
 */

const { contextBridge, ipcMain } = require('electron');

contextBridge.exposeInMainWorld('electron', {
  getServerUrl: () => ipcMain.invoke('get-server-url'),
  getAppVersion: () => ipcMain.invoke('get-app-version'),
  minimizeWindow: () => ipcMain.invoke('minimize-window'),
  maximizeWindow: () => ipcMain.invoke('maximize-window'),
  closeWindow: () => ipcMain.invoke('close-window')
});
