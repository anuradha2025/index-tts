// Background service worker for IndexTTS extension
let isProcessing = false;
let currentAudio = null;

// Listen for messages from content script
chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  if (message.action === 'generateSpeech') {
    handleTextToSpeech(message.text, sendResponse);
    return true; // Keep message channel open for async response
  } else if (message.action === 'stopSpeech') {
    stopCurrentAudio();
    sendResponse({ success: true });
  } else if (message.action === 'isProcessing') {
    sendResponse({ processing: isProcessing });
  }
});

async function handleTextToSpeech(text, sendResponse) {
  if (isProcessing) {
    sendResponse({ error: 'Already processing another request' });
    return;
  }

  isProcessing = true;
  
  try {
    // Get settings from storage
    const settings = await chrome.storage.sync.get({
      voice: 'default',
      speed: 1.0,
      volume: 1.0,
      autoPlay: true
    });

    // Send request to native messaging host
    const response = await sendNativeMessage({
      action: 'synthesize',
      text: text,
      settings: settings
    });

    if (response.success) {
      sendResponse({ 
        success: true, 
        audioData: response.audioData,
        audioUrl: response.audioUrl 
      });
    } else {
      sendResponse({ error: response.error || 'Unknown error occurred' });
    }
  } catch (error) {
    console.error('TTS Error:', error);
    sendResponse({ error: error.message });
  } finally {
    isProcessing = false;
  }
}

function sendNativeMessage(message) {
  return new Promise((resolve, reject) => {
    chrome.runtime.sendNativeMessage('com.indextts.host', message, (response) => {
      if (chrome.runtime.lastError) {
        reject(new Error(chrome.runtime.lastError.message));
      } else {
        resolve(response);
      }
    });
  });
}

function stopCurrentAudio() {
  if (currentAudio) {
    currentAudio.pause();
    currentAudio = null;
  }
}

// Handle extension icon click
chrome.action.onClicked.addListener((tab) => {
  chrome.tabs.sendMessage(tab.id, { action: 'toggleReader' });
});

// Initialize extension
chrome.runtime.onInstalled.addListener(() => {
  // Set default settings
  chrome.storage.sync.set({
    voice: 'default',
    speed: 1.0,
    volume: 1.0,
    autoPlay: true,
    highlightText: true
  });
});