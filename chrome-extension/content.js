// Content script for text extraction and reading
class IndexTTSReader {
  constructor() {
    this.isActive = false;
    this.selectedText = '';
    this.isPlaying = false;
    this.currentAudio = null;
    this.readingPosition = 0;
    this.setupEventListeners();
    this.createFloatingControls();
  }

  setupEventListeners() {
    // Listen for text selection
    document.addEventListener('mouseup', () => {
      const selection = window.getSelection();
      if (selection.toString().trim().length > 0) {
        this.selectedText = selection.toString().trim();
        this.showFloatingControls(true);
      } else {
        this.showFloatingControls(false);
      }
    });

    // Listen for messages from background script
    chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
      if (message.action === 'toggleReader') {
        this.toggleReader();
      } else if (message.action === 'readPage') {
        this.readEntirePage();
      }
      sendResponse({ success: true });
    });

    // Keyboard shortcuts
    document.addEventListener('keydown', (e) => {
      if (e.ctrlKey && e.shiftKey && e.key === 'R') {
        e.preventDefault();
        this.readSelectedOrPage();
      } else if (e.ctrlKey && e.shiftKey && e.key === 'S') {
        e.preventDefault();
        this.stopReading();
      }
    });
  }

  createFloatingControls() {
    this.floatingDiv = document.createElement('div');
    this.floatingDiv.id = 'indextts-floating-controls';
    this.floatingDiv.style.cssText = `
      position: fixed;
      top: 10px;
      right: 10px;
      background: #2c3e50;
      color: white;
      padding: 10px;
      border-radius: 8px;
      box-shadow: 0 4px 12px rgba(0,0,0,0.3);
      z-index: 10000;
      font-family: Arial, sans-serif;
      font-size: 14px;
      display: none;
      min-width: 200px;
    `;

    this.floatingDiv.innerHTML = `
      <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 8px;">
        <span style="font-weight: bold;">🔊 IndexTTS</span>
        <button id="indextts-close" style="background: none; border: none; color: white; cursor: pointer; font-size: 16px;">×</button>
      </div>
      <div style="display: flex; gap: 8px; flex-wrap: wrap;">
        <button id="indextts-read-selection" class="indextts-btn">Read Selection</button>
        <button id="indextts-read-page" class="indextts-btn">Read Page</button>
        <button id="indextts-stop" class="indextts-btn">Stop</button>
        <button id="indextts-settings" class="indextts-btn">Settings</button>
      </div>
      <div id="indextts-status" style="margin-top: 8px; font-size: 12px; opacity: 0.8;"></div>
    `;

    const btnStyle = `
      background: #3498db;
      color: white;
      border: none;
      padding: 6px 12px;
      border-radius: 4px;
      cursor: pointer;
      font-size: 12px;
      transition: background 0.3s;
    `;

    document.head.appendChild(document.createElement('style')).textContent = `
      .indextts-btn {
        ${btnStyle}
      }
      .indextts-btn:hover {
        background: #2980b9 !important;
      }
      .indextts-btn:disabled {
        background: #7f8c8d !important;
        cursor: not-allowed !important;
      }
    `;

    document.body.appendChild(this.floatingDiv);

    // Add event listeners
    document.getElementById('indextts-close').addEventListener('click', () => {
      this.showFloatingControls(false);
    });

    document.getElementById('indextts-read-selection').addEventListener('click', () => {
      this.readSelectedText();
    });

    document.getElementById('indextts-read-page').addEventListener('click', () => {
      this.readEntirePage();
    });

    document.getElementById('indextts-stop').addEventListener('click', () => {
      this.stopReading();
    });

    document.getElementById('indextts-settings').addEventListener('click', () => {
      this.openSettings();
    });
  }

  showFloatingControls(show) {
    if (this.floatingDiv) {
      this.floatingDiv.style.display = show ? 'block' : 'none';
    }
  }

  toggleReader() {
    this.isActive = !this.isActive;
    this.showFloatingControls(this.isActive);
  }

  readSelectedOrPage() {
    if (this.selectedText) {
      this.readSelectedText();
    } else {
      this.readEntirePage();
    }
  }

  async readSelectedText() {
    if (!this.selectedText) {
      this.updateStatus('No text selected');
      return;
    }
    await this.synthesizeAndPlay(this.selectedText);
  }

  async readEntirePage() {
    const pageText = this.extractPageText();
    if (!pageText) {
      this.updateStatus('No readable text found on page');
      return;
    }
    await this.synthesizeAndPlay(pageText);
  }

  extractPageText() {
    // Remove script and style elements
    const clonedDoc = document.cloneNode(true);
    const scripts = clonedDoc.querySelectorAll('script, style, nav, header, footer, aside');
    scripts.forEach(el => el.remove());

    // Get main content
    let content = clonedDoc.querySelector('main, article, [role="main"], .content, #content');
    if (!content) {
      content = clonedDoc.querySelector('body');
    }

    // Extract text and clean it
    let text = content.textContent || content.innerText || '';
    text = text.replace(/\s+/g, ' ').trim();
    
    // Limit text length for processing
    const maxLength = 5000;
    if (text.length > maxLength) {
      text = text.substring(0, maxLength) + '...';
    }

    return text;
  }

  async synthesizeAndPlay(text) {
    if (this.isPlaying) {
      this.updateStatus('Already playing...');
      return;
    }

    this.updateStatus('Generating speech...');
    this.setButtonsEnabled(false);

    try {
      const response = await chrome.runtime.sendMessage({
        action: 'generateSpeech',
        text: text
      });

      if (response.success) {
        await this.playAudio(response.audioUrl || response.audioData);
        this.updateStatus('Playing...');
      } else {
        this.updateStatus('Error: ' + (response.error || 'Unknown error'));
      }
    } catch (error) {
      console.error('TTS Error:', error);
      this.updateStatus('Error: ' + error.message);
    } finally {
      this.setButtonsEnabled(true);
    }
  }

  async playAudio(audioSource) {
    return new Promise((resolve, reject) => {
      this.currentAudio = new Audio();
      
      if (audioSource.startsWith('data:')) {
        this.currentAudio.src = audioSource;
      } else {
        this.currentAudio.src = chrome.runtime.getURL('audio/' + audioSource);
      }

      this.currentAudio.onloadeddata = () => {
        this.isPlaying = true;
        this.currentAudio.play();
      };

      this.currentAudio.onended = () => {
        this.isPlaying = false;
        this.updateStatus('Finished');
        resolve();
      };

      this.currentAudio.onerror = (error) => {
        this.isPlaying = false;
        this.updateStatus('Audio playback error');
        reject(error);
      };
    });
  }

  stopReading() {
    if (this.currentAudio) {
      this.currentAudio.pause();
      this.currentAudio = null;
    }
    this.isPlaying = false;
    this.updateStatus('Stopped');
    chrome.runtime.sendMessage({ action: 'stopSpeech' });
  }

  updateStatus(message) {
    const statusEl = document.getElementById('indextts-status');
    if (statusEl) {
      statusEl.textContent = message;
    }
  }

  setButtonsEnabled(enabled) {
    const buttons = document.querySelectorAll('.indextts-btn');
    buttons.forEach(btn => {
      btn.disabled = !enabled;
    });
  }

  openSettings() {
    // Send message to open settings GUI
    chrome.runtime.sendMessage({ action: 'openSettings' });
  }
}

// Initialize the reader when page loads
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', () => {
    new IndexTTSReader();
  });
} else {
  new IndexTTSReader();
}