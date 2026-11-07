/* ═══════════════════════════════════════════════════
   Activity Recognition — Frontend JavaScript
   ═══════════════════════════════════════════════════ */

// ── Tab switching ──────────────────────────────────
function showTab(name) {
  document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
  document.querySelectorAll('.tab-content').forEach(s => s.classList.remove('active'));
  document.querySelector(`#tab-${name}`).classList.add('active');
  event.currentTarget.classList.add('active');
}

// ── Live Camera ────────────────────────────────────
let mediaStream = null;
let captureInterval = null;
let frameBuffer = [];
let lastPredTime = Date.now();
let predCount = 0;

async function startCamera() {
  try {
    mediaStream = await navigator.mediaDevices.getUserMedia({
      video: { width: 640, height: 480, facingMode: 'user' },
      audio: false
    });

    const video = document.getElementById('videoEl');
    video.srcObject = mediaStream;
    video.style.display = 'block';
    document.getElementById('cameraPlaceholder').style.display = 'none';
    document.getElementById('liveOverlay').style.display = 'block';

    document.getElementById('startBtn').style.display = 'none';
    document.getElementById('stopBtn').style.display = 'inline-flex';

    // Capture a frame every 300ms → build buffer of 16 frames
    captureInterval = setInterval(captureFrame, 300);

  } catch (err) {
    alert('Camera access denied or not available: ' + err.message);
  }
}

function stopCamera() {
  clearInterval(captureInterval);
  captureInterval = null;
  frameBuffer = [];

  if (mediaStream) {
    mediaStream.getTracks().forEach(t => t.stop());
    mediaStream = null;
  }

  const video = document.getElementById('videoEl');
  video.style.display = 'none';
  video.srcObject = null;
  document.getElementById('cameraPlaceholder').style.display = 'flex';
  document.getElementById('liveOverlay').style.display = 'none';

  document.getElementById('startBtn').style.display = 'inline-flex';
  document.getElementById('stopBtn').style.display = 'none';

  document.getElementById('predLabel').textContent = '—';
  document.getElementById('predConf').textContent = '—';
  document.getElementById('predFps').textContent = '—';
  document.getElementById('confBar').style.width = '0%';
  document.getElementById('overlayLabel').textContent = '—';
  document.getElementById('overlayConf').textContent = '';
}

function captureFrame() {
  const video  = document.getElementById('videoEl');
  const canvas = document.getElementById('canvasEl');
  if (!video.videoWidth) return;

  canvas.width  = 112;
  canvas.height = 112;
  const ctx = canvas.getContext('2d');
  ctx.drawImage(video, 0, 0, 112, 112);

  const dataUrl = canvas.toDataURL('image/jpeg', 0.7);
  frameBuffer.push(dataUrl);
  if (frameBuffer.length > 16) frameBuffer.shift();

  // Send to server when we have 8+ frames (predict every new frame after that)
  if (frameBuffer.length >= 8) {
    sendFrames([...frameBuffer]);
  }
}

let isPredicting = false;

async function sendFrames(frames) {
  if (isPredicting) return;
  isPredicting = true;

  try {
    const res = await fetch('/api/predict_frame', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ frames })
    });
    const data = await res.json();

    // FPS
    const now = Date.now();
    const fps = (1000 / (now - lastPredTime)).toFixed(1);
    lastPredTime = now;

    updatePredUI(data.label, data.confidence, fps);
  } catch (e) {
    console.error('Prediction error:', e);
  } finally {
    isPredicting = false;
  }
}

const activityColors = {
  'Sitting / Idle': '#06b6d4',
  'Walking':        '#16a34a',
  'Running':        '#dc2626',
  'Jumping':        '#7c3aed',
};

function updatePredUI(label, conf, fps) {
  document.getElementById('predLabel').textContent = label;
  document.getElementById('predConf').textContent  = (conf * 100).toFixed(1) + '%';
  document.getElementById('predFps').textContent   = fps;
  document.getElementById('confBar').style.width   = (conf * 100) + '%';
  document.getElementById('overlayLabel').textContent = label;
  document.getElementById('overlayConf').textContent  = (conf * 100).toFixed(1) + '% confidence';

  const color = activityColors[label] || '#3b82f6';
  document.getElementById('predLabel').style.color = color;
  document.getElementById('overlayLabel').style.color = color;

  // Log entry
  const log = document.getElementById('predLog');
  const time = new Date().toLocaleTimeString();
  const entry = document.createElement('div');
  entry.className = 'log-entry';
  entry.textContent = `[${time}]  ${label}  — ${(conf * 100).toFixed(1)}%`;
  log.prepend(entry);

  // Keep log to 30 entries
  while (log.children.length > 30) log.removeChild(log.lastChild);
}

// ── Upload Video ───────────────────────────────────
function handleDrop(e) {
  e.preventDefault();
  document.getElementById('dropZone').classList.remove('drag-over');
  const file = e.dataTransfer.files[0];
  if (file) handleFile(file);
}

async function handleFile(file) {
  if (!file) return;

  const allowed = ['video/mp4', 'video/avi', 'video/quicktime', 'video/x-matroska', 'video/x-msvideo'];
  if (!allowed.includes(file.type) && !file.name.match(/\.(mp4|avi|mov|mkv)$/i)) {
    alert('Please upload a valid video file (MP4, AVI, MOV, MKV).');
    return;
  }

  const statusBox  = document.getElementById('uploadStatus');
  const statusText = document.getElementById('uploadStatusText');
  const resultBox  = document.getElementById('uploadResult');

  statusBox.style.display = 'flex';
  resultBox.style.display = 'none';
  statusText.textContent = `Uploading "${file.name}"…`;

  const formData = new FormData();
  formData.append('video', file);

  try {
    const res = await fetch('/api/predict_video', {
      method: 'POST',
      body: formData
    });

    if (!res.ok) {
      const err = await res.json();
      throw new Error(err.error || 'Server error');
    }

    const data = await res.json();
    statusBox.style.display = 'none';
    resultBox.style.display = 'block';

    document.getElementById('uploadLabel').textContent  = data.label;
    document.getElementById('uploadConf').textContent   = (data.confidence * 100).toFixed(1) + '%';
    document.getElementById('uploadFrames').textContent = data.frames_analyzed;

    const color = activityColors[data.label] || '#2563eb';
    document.getElementById('uploadLabel').style.color = color;

  } catch (err) {
    statusBox.style.display = 'none';
    alert('Error: ' + err.message);
  }
}
