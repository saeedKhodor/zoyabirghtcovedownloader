# === CODE INDEX ===
# get_html_page()                          Line 12

"""
Self-contained HTML5, CSS3, and JavaScript Single Page Interface
for the Localhost Brightcove Video Downloader.
"""


def get_html_page() -> str:
    """Returns the complete HTML string for the web dashboard."""
    return """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Brightcove Video Downloader</title>
  <style>
    :root {
      --bg: #F5F5F7;
      --card: #FFFFFF;
      --text: #1D1D1F;
      --text-sec: #6E6E73;
      --primary: #0071E3;
      --primary-hover: #0077ED;
      --danger: #FF3B30;
      --success: #34C759;
      --border: #D2D2D7;
      --terminal-bg: #1C1C1E;
      --terminal-text: #F2F2F7;
    }

    * { box-sizing: border-box; margin: 0; padding: 0; }
    body {
      font-family: -apple-system, BlinkMacSystemFont, "SF Pro Display", "SF Pro Text", "Helvetica Neue", sans-serif;
      background: var(--bg);
      color: var(--text);
      display: flex;
      justify-content: center;
      padding: 40px 20px;
      min-height: 100vh;
      -webkit-font-smoothing: antialiased;
    }

    .container {
      width: 100%;
      max-width: 620px;
    }

    .header {
      text-align: center;
      margin-bottom: 28px;
    }

    .header h1 {
      font-size: 28px;
      font-weight: 700;
      letter-spacing: -0.5px;
      margin-bottom: 6px;
    }

    .header p {
      color: var(--text-sec);
      font-size: 14px;
    }

    .card {
      background: var(--card);
      border-radius: 18px;
      padding: 28px;
      box-shadow: 0 4px 24px rgba(0, 0, 0, 0.06);
      border: 1px solid rgba(0, 0, 0, 0.04);
      margin-bottom: 24px;
    }

    .form-group {
      margin-bottom: 18px;
    }

    .form-group label {
      display: block;
      font-size: 13px;
      font-weight: 600;
      margin-bottom: 6px;
      color: var(--text);
    }

    .form-group input, .form-group select {
      width: 100%;
      padding: 12px 14px;
      font-size: 15px;
      border: 1px solid var(--border);
      border-radius: 10px;
      background: #FAFAFA;
      color: var(--text);
      outline: none;
      transition: all 0.2s ease;
    }

    .form-group input:focus, .form-group select:focus {
      border-color: var(--primary);
      background: #FFFFFF;
      box-shadow: 0 0 0 3px rgba(0, 113, 227, 0.15);
    }

    .form-row {
      display: flex;
      gap: 12px;
    }
    .form-row .form-group { flex: 1; }

    .btn-row {
      display: flex;
      gap: 12px;
      margin-top: 24px;
    }

    button {
      flex: 1;
      padding: 14px;
      font-size: 15px;
      font-weight: 600;
      border: none;
      border-radius: 12px;
      cursor: pointer;
      transition: all 0.2s ease;
    }

    .btn-primary {
      background: var(--primary);
      color: #FFFFFF;
    }
    .btn-primary:hover:not(:disabled) {
      background: var(--primary-hover);
      transform: translateY(-1px);
    }

    .btn-secondary {
      background: #E5E5EA;
      color: var(--text);
      flex: 0 0 110px;
    }
    .btn-secondary:hover:not(:disabled) {
      background: #D1D1D6;
    }

    button:disabled {
      opacity: 0.5;
      cursor: not-allowed;
      transform: none !important;
    }

    /* Progress & Metrics */
    .progress-box {
      margin-top: 20px;
      display: none;
    }

    .progress-metrics {
      display: flex;
      justify-content: space-between;
      font-size: 13px;
      font-weight: 600;
      color: var(--text-sec);
      margin-bottom: 8px;
    }

    .progress-bar-bg {
      height: 10px;
      background: #E5E5EA;
      border-radius: 6px;
      overflow: hidden;
    }

    .progress-bar-fill {
      height: 100%;
      width: 0%;
      background: var(--primary);
      border-radius: 6px;
      transition: width 0.2s ease;
    }

    .status-text {
      font-size: 13px;
      color: var(--text-sec);
      margin-top: 8px;
      text-align: center;
    }

    /* Log Console */
    .log-card {
      background: var(--terminal-bg);
      border-radius: 14px;
      padding: 16px;
      color: var(--terminal-text);
      font-family: ui-monospace, Menlo, Monaco, Consolas, monospace;
      font-size: 12px;
      max-height: 200px;
      overflow-y: auto;
      white-space: pre-wrap;
      word-break: break-all;
    }

    .badge {
      display: inline-block;
      padding: 4px 8px;
      border-radius: 6px;
      font-size: 12px;
      font-weight: 600;
    }
    .badge-success { background: rgba(52, 199, 89, 0.15); color: #28a745; }
    .badge-danger { background: rgba(255, 59, 48, 0.15); color: #dc3545; }
  </style>
</head>
<body>
  <div class="container">
    <div class="header">
      <h1>Brightcove Video Downloader</h1>
      <p>Local Web Dashboard &bull; Downloads automatically to your <strong>Downloads</strong> folder</p>
    </div>

    <div class="card">
      <div class="form-group">
        <label for="accountId">Account ID</label>
        <input type="text" id="accountId" value="3887645559001" placeholder="e.g. 3887645559001">
      </div>

      <div class="form-row">
        <div class="form-group">
          <label for="playerId">Player ID</label>
          <input type="text" id="playerId" value="default" placeholder="default or player ID">
        </div>

        <div class="form-group">
          <label for="quality">Quality</label>
          <select id="quality">
            <option value="best" selected>Best Available (Default)</option>
            <option value="1080p">1080p</option>
            <option value="720p">720p</option>
            <option value="480p">480p</option>
            <option value="audio">Audio Only</option>
          </select>
        </div>
      </div>

      <div class="form-group">
        <label for="videoId">Video ID</label>
        <input type="text" id="videoId" value="5978804382001" placeholder="e.g. 5978804382001">
      </div>

      <div class="btn-row">
        <button id="downloadBtn" class="btn-primary" onclick="startDownload()">Download Video</button>
        <button id="cancelBtn" class="btn-secondary" onclick="cancelDownload()" disabled>Cancel</button>
      </div>

      <div id="progressBox" class="progress-box">
        <div class="progress-metrics">
          <span id="percentText">0.0%</span>
          <span id="speedEtaText">Speed: -- | ETA: --</span>
        </div>
        <div class="progress-bar-bg">
          <div id="progressBar" class="progress-bar-fill"></div>
        </div>
        <div id="statusText" class="status-text">Preparing download...</div>
      </div>
    </div>

    <div class="card">
      <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
        <span style="font-size: 13px; font-weight: 600;">Activity Log</span>
        <button onclick="openFolder()" style="flex: none; padding: 6px 12px; font-size: 12px; border-radius: 8px; background: #E5E5EA;">Open Downloads Folder</button>
      </div>
      <div id="logConsole" class="log-card">Brightcove Downloader Local Server Ready.
Awaiting your download request...
</div>
    </div>
  </div>

  <script>
    let pollInterval = null;

    async function startDownload() {
      const accountId = document.getElementById('accountId').value.trim();
      const playerId = document.getElementById('playerId').value.trim();
      const videoId = document.getElementById('videoId').value.trim();
      const quality = document.getElementById('quality').value;

      if (!accountId || !videoId) {
        alert("Please provide both Account ID and Video ID.");
        return;
      }

      document.getElementById('downloadBtn').disabled = true;
      document.getElementById('cancelBtn').disabled = false;
      document.getElementById('progressBox').style.display = 'block';
      document.getElementById('progressBar').style.width = '0%';
      document.getElementById('percentText').innerText = '0.0%';
      document.getElementById('statusText').innerText = 'Connecting to Brightcove...';

      try {
        const res = await fetch('/api/download', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ account_id: accountId, player_id: playerId, video_id: videoId, quality: quality })
        });
        const data = await res.json();
        if (data.status === 'started') {
          if (!pollInterval) pollInterval = setInterval(checkStatus, 700);
        } else {
          alert(data.error || 'Failed to start download');
          resetControls();
        }
      } catch (err) {
        alert('Server connection error: ' + err);
        resetControls();
      }
    }

    async function checkStatus() {
      try {
        const res = await fetch('/api/status');
        const data = await res.json();

        // Update progress bar
        const pct = data.percent || 0;
        document.getElementById('progressBar').style.width = pct + '%';
        document.getElementById('percentText').innerText = pct.toFixed(1) + '%';
        document.getElementById('speedEtaText').innerText = `Speed: ${data.speed || '--'} | ETA: ${data.eta || '--'}`;
        document.getElementById('statusText').innerText = data.message || '';

        // Update logs
        if (data.logs && data.logs.length > 0) {
          const consoleEl = document.getElementById('logConsole');
          consoleEl.innerText = data.logs.join('\\n');
          consoleEl.scrollTop = consoleEl.scrollHeight;
        }

        // Completion states
        if (data.status === 'completed') {
          clearInterval(pollInterval);
          pollInterval = null;
          resetControls();
          document.getElementById('statusText').innerHTML = '<span class="badge badge-success">✓ Download Finished! Check your Downloads folder.</span>';
        } else if (data.status === 'error' || data.status === 'cancelled') {
          clearInterval(pollInterval);
          pollInterval = null;
          resetControls();
          document.getElementById('statusText').innerHTML = `<span class="badge badge-danger">${data.message}</span>`;
        }
      } catch (e) {
        console.error('Polling error', e);
      }
    }

    async function cancelDownload() {
      document.getElementById('cancelBtn').disabled = true;
      document.getElementById('statusText').innerText = 'Cancelling download...';
      await fetch('/api/cancel', { method: 'POST' });
    }

    async function openFolder() {
      await fetch('/api/open-folder', { method: 'POST' });
    }

    function resetControls() {
      document.getElementById('downloadBtn').disabled = false;
      document.getElementById('cancelBtn').disabled = true;
    }
  </script>
</body>
</html>
"""
