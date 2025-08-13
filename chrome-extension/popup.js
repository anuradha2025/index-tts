// Popup script for IndexTTS extension
document.addEventListener('DOMContentLoaded', function() {
  const statusDiv = document.getElementById('status');
  const readSelectionBtn = document.getElementById('readSelection');
  const readPageBtn = document.getElementById('readPage');
  const stopReadingBtn = document.getElementById('stopReading');
  const openSettingsBtn = document.getElementById('openSettings');

  // Update status
  function updateStatus(message, type = 'ready') {
    statusDiv.textContent = message;
    statusDiv.className = `status ${type}`;
  }

  // Check if background script is processing
  chrome.runtime.sendMessage({ action: 'isProcessing' }, (response) => {
    if (response && response.processing) {
      updateStatus('Processing...', 'processing');
      setButtonsEnabled(false);
    }
  });

  // Button event handlers
  readSelectionBtn.addEventListener('click', () => {
    sendToActiveTab('readSelection');
  });

  readPageBtn.addEventListener('click', () => {
    sendToActiveTab('readPage');
  });

  stopReadingBtn.addEventListener('click', () => {
    chrome.runtime.sendMessage({ action: 'stopSpeech' }, (response) => {
      updateStatus('Stopped', 'ready');
      setButtonsEnabled(true);
    });
    sendToActiveTab('stopReading');
  });

  openSettingsBtn.addEventListener('click', () => {
    // Launch settings application
    chrome.runtime.sendNativeMessage('com.indextts.host', {
      action: 'openSettings'
    }, (response) => {
      if (chrome.runtime.lastError) {
        updateStatus('Settings app not available', 'error');
      } else {
        updateStatus('Settings opened', 'ready');
      }
    });
  });

  function sendToActiveTab(action) {
    chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {
      if (tabs[0]) {
        chrome.tabs.sendMessage(tabs[0].id, {action: action}, function(response) {
          if (chrome.runtime.lastError) {
            updateStatus('Error: Could not connect to page', 'error');
          }
        });
      }
    });
  }

  function setButtonsEnabled(enabled) {
    readSelectionBtn.disabled = !enabled;
    readPageBtn.disabled = !enabled;
    if (enabled) {
      readSelectionBtn.className = 'btn btn-primary';
      readPageBtn.className = 'btn btn-primary';
    } else {
      readSelectionBtn.className = 'btn btn-secondary';
      readPageBtn.className = 'btn btn-secondary';
    }
  }

  // Listen for background script messages
  chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
    if (message.action === 'statusUpdate') {
      updateStatus(message.status, message.type || 'ready');
      setButtonsEnabled(message.enabled !== false);
    }
  });
});