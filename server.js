const express = require("express");
const cors = require("cors");
const path = require("path");
const si = require("systeminformation");
const { exec } = require("child_process");
const Database = require("better-sqlite3");

require("dotenv").config();

const app = express();
const PORT = process.env.PORT || 3000;

app.use(cors());
app.use(express.json());

// Serve frontend static files
app.use(express.static(path.join(__dirname, "public")));

// Initialize Database
const db = new Database('memory.db');
db.exec(`
  CREATE TABLE IF NOT EXISTS messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    role TEXT,
    content TEXT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
  )
`);

// Middleware Keamanan API
const authenticate = (req, res, next) => {
    const apiKey = req.headers['x-api-key'] || req.query.key;
    const expectedKey = process.env.JARVIS_API_KEY || "jarvis_secure_access_token_2026";
    
    // Izinkan jika request dari localhost (frontend sendiri) tanpa key, 
    // atau jika key cocok.
    const isLocal = req.hostname === 'localhost' || req.hostname === '127.0.0.1';

    if (apiKey === expectedKey || isLocal) {
        next();
    } else {
        res.status(401).json({ error: "Akses ditolak: API Key tidak valid" });
    }
};

// Endpoint untuk mengambil history (max 50)
app.get("/api/history", authenticate, (req, res) => {
    try {
        const rows = db.prepare("SELECT role, content, timestamp FROM messages ORDER BY id DESC LIMIT 50").all();
        res.json({ history: rows.reverse() });
    } catch (err) {
        console.error("DB error:", err);
        res.status(500).json({ error: "Failed to load history" });
    }
});

// Endpoint untuk menghapus history
app.delete("/api/history", (req, res) => {
    try {
        db.prepare("DELETE FROM messages").run();
        res.json({ success: true, message: "Memory cleared" });
    } catch (err) {
        res.status(500).json({ error: "Failed to clear memory" });
    }
});

// Proxy endpoint ke Google Gemini API
app.post("/api/chat", authenticate, async (req, res) => {
    const { messages, system } = req.body;

    if (!messages || !Array.isArray(messages)) {
        return res.status(400).json({ error: "Field 'messages' harus berupa array." });
    }

    // Perintah khusus hapus ingatan
    const lastMsg = messages[messages.length - 1];
    if (lastMsg && lastMsg.role === "user" && lastMsg.content.toLowerCase().includes("jarvis, hapus ingatanmu")) {
        try {
            db.prepare("DELETE FROM messages").run();
            const reply = "Ingatan telah dibersihkan, Boss.";
            return res.json({ reply });
        } catch (e) {
            return res.status(500).json({ error: "Gagal menghapus ingatan." });
        }
    }

    const apiKey = process.env.GEMINI_API_KEY;
    if (!apiKey) {
        return res.status(500).json({ error: "GEMINI_API_KEY belum diset di .env" });
    }

    try {
        // Convert format messages ke Gemini style
        const geminiContents = messages.map((msg) => {
            const parts = [{ text: msg.content }];
            if (msg.imageBase64) {
                const base64Data = msg.imageBase64.replace(/^data:image\/\w+;base64,/, '');
                parts.push({
                    inlineData: {
                        data: base64Data,
                        mimeType: "image/jpeg"
                    }
                });
            }
            return {
                role: msg.role === "assistant" ? "model" : "user",
                parts: parts,
            };
        });

        const body = {
            contents: geminiContents,
            generationConfig: {
                maxOutputTokens: 8192,
                temperature: 0.9,
            },
        };

        // System prompt masuk ke systemInstruction
        if (system) {
            body.systemInstruction = {
                parts: [{ text: system }],
            };
        }

        const model = process.env.GEMINI_MODEL || "gemini-3.1-flash-lite";
        const url = `https://generativelanguage.googleapis.com/v1beta/models/${model}:generateContent?key=${apiKey}`;

        const response = await fetch(url, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(body),
        });

        const data = await response.json();

        if (!response.ok) {
            return res.status(response.status).json({ error: data?.error?.message || "Gemini API error" });
        }

        const reply = data?.candidates?.[0]?.content?.parts?.[0]?.text || "Tidak ada respons.";

        try {
            const stmt = db.prepare("INSERT INTO messages (role, content) VALUES (?, ?)");
            const lastUserMsg = messages[messages.length - 1];
            if (lastUserMsg && lastUserMsg.role === "user") {
                stmt.run("user", lastUserMsg.content);
            }
            stmt.run("assistant", reply);
        } catch (e) { console.error("Failed to save to DB", e); }

        res.json({ reply });

    } catch (err) {
        console.error("Server error:", err);
        res.status(500).json({ error: "Internal server error: " + err.message });
    }
});

// Proxy endpoint ke Google Gemini API (STREAMING)
app.post("/api/chat/stream", authenticate, async (req, res) => {
    const { messages, system } = req.body;

    if (!messages || !Array.isArray(messages)) {
        return res.status(400).json({ error: "Field 'messages' harus berupa array." });
    }

    // Perintah khusus hapus ingatan
    const lastMsg = messages[messages.length - 1];
    if (lastMsg && lastMsg.role === "user" && lastMsg.content.toLowerCase().includes("jarvis, hapus ingatanmu")) {
        try {
            db.prepare("DELETE FROM messages").run();
            const reply = "Ingatan telah dibersihkan, Boss.";

            res.setHeader('Content-Type', 'text/event-stream');
            res.setHeader('Cache-Control', 'no-cache');
            res.setHeader('Connection', 'keep-alive');

            res.write(`data: ${JSON.stringify({ token: reply })}\n\n`);
            res.write('data: [DONE]\n\n');
            res.end();
            return;
        } catch (e) {
            return res.status(500).json({ error: "Gagal menghapus ingatan." });
        }
    }

    const apiKey = process.env.GEMINI_API_KEY;
    if (!apiKey) {
        return res.status(500).json({ error: "GEMINI_API_KEY belum diset di .env" });
    }

    try {
        const geminiContents = messages.map((msg) => {
            const parts = [{ text: msg.content }];
            if (msg.imageBase64) {
                const base64Data = msg.imageBase64.replace(/^data:image\/\w+;base64,/, '');
                parts.push({
                    inlineData: {
                        data: base64Data,
                        mimeType: "image/jpeg"
                    }
                });
            }
            return {
                role: msg.role === "assistant" ? "model" : "user",
                parts: parts,
            };
        });

        const body = {
            contents: geminiContents,
            generationConfig: {
                maxOutputTokens: 8192,
                temperature: 0.9,
            },
        };

        if (system) {
            body.systemInstruction = {
                parts: [{ text: system }],
            };
        }

        const model = process.env.GEMINI_MODEL || "Claude Opus 4.6";
        const url = `https://generativelanguage.googleapis.com/v1beta/models/${model}:streamGenerateContent?key=${apiKey}`;

        const response = await fetch(url, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(body),
        });

        if (!response.ok) {
            const data = await response.json();
            return res.status(response.status).json({ error: data?.error?.message || "Gemini API error" });
        }

        // Set header untuk SSE
        res.setHeader('Content-Type', 'text/event-stream');
        res.setHeader('Cache-Control', 'no-cache');
        res.setHeader('Connection', 'keep-alive');

        const reader = response.body.getReader();
        const decoder = new TextDecoder();
        let buffer = '';
        let braceCount = 0;
        let startIndex = -1;
        let fullReply = "";

        while (true) {
            const { done, value } = await reader.read();
            if (done) break;

            const chunk = decoder.decode(value, { stream: true });
            for (let i = 0; i < chunk.length; i++) {
                const char = chunk[i];
                if (char === '{') {
                    if (braceCount === 0) {
                        startIndex = buffer.length;
                    }
                    braceCount++;
                }

                buffer += char;

                if (char === '}') {
                    braceCount--;
                    if (braceCount === 0 && startIndex !== -1) {
                        const jsonStr = buffer.substring(startIndex);
                        try {
                            const json = JSON.parse(jsonStr);
                            const token = json?.candidates?.[0]?.content?.parts?.[0]?.text;
                            if (token) {
                                fullReply += token;
                                res.write(`data: ${JSON.stringify({ token })}\n\n`);
                            }
                        } catch (e) {
                            // Ignored: might be partial or invalid JSON
                        }
                        // Reset for next object
                        buffer = '';
                        startIndex = -1;
                    }
                }
            }
        }

        res.write('data: [DONE]\n\n');

        try {
            const stmt = db.prepare("INSERT INTO messages (role, content) VALUES (?, ?)");
            const lastUserMsg = messages[messages.length - 1];
            if (lastUserMsg && lastUserMsg.role === "user") {
                stmt.run("user", lastUserMsg.content);
            }
            stmt.run("assistant", fullReply);
        } catch (e) { console.error("Failed to save to DB", e); }

        res.end();

    } catch (err) {
        console.error("Streaming error:", err);
        // If headers already sent, we can't send status 500
        if (!res.headersSent) {
            res.status(500).json({ error: "Internal server error: " + err.message });
        } else {
            res.write(`data: ${JSON.stringify({ error: err.message })}\n\n`);
            res.end();
        }
    }
});

// Endpoint untuk Kendali Sistem (Shutdown/Sleep)
app.post("/api/system/control", authenticate, (req, res) => {
    const { action } = req.body;

    if (action === "shutdown") {
        console.log("JARVIS: Initiating Shutdown...");
        // shutdown /s = shutdown, /t 30 = delay 30s
        exec("shutdown /s /t 30", (err) => {
            if (err) return res.status(500).json({ error: "Gagal mematikan sistem" });
        });
        return res.json({ success: true, message: "Shutdown sequence initiated (30s)" });
    }

    if (action === "sleep") {
        console.log("JARVIS: Entering Sleep Mode...");
        // Menggunakan PowerShell untuk memastikan mode Sleep (bukan Hibernate)
        const sleepCmd = `powershell -Command "Add-Type -AssemblyName System.Windows.Forms; [System.Windows.Forms.Application]::SetSuspendState([System.Windows.Forms.PowerState]::Suspend, $false, $false)"`;
        exec(sleepCmd, (err) => {
            if (err) return res.status(500).json({ error: "Gagal masuk mode tidur" });
        });
        return res.json({ success: true, message: "System entering sleep mode" });
    }

    if (action === "restart") {
        console.log("JARVIS: Initiating Restart...");
        exec("shutdown /r /t 30", (err) => {
            if (err) return res.status(500).json({ error: "Gagal restart sistem" });
        });
        return res.json({ success: true, message: "Restart sequence initiated (30s)" });
    }

    if (action === "lock") {
        console.log("JARVIS: Locking System...");
        exec("rundll32.exe user32.dll,LockWorkStation", (err) => {
            if (err) return res.status(500).json({ error: "Gagal mengunci sistem" });
        });
        return res.json({ success: true, message: "System locked" });
    }

    if (action === "volume_up") {
        exec('powershell -Command "(new-object -com wscript.shell).SendKeys([char]175)"', (err) => {
            if (err) return res.status(500).json({ error: "Gagal menaikkan volume" });
        });
        return res.json({ success: true, message: "Volume increased" });
    }

    if (action === "volume_down") {
        exec('powershell -Command "(new-object -com wscript.shell).SendKeys([char]174)"', (err) => {
            if (err) return res.status(500).json({ error: "Gagal menurunkan volume" });
        });
        return res.json({ success: true, message: "Volume decreased" });
    }

    if (action === "volume_mute") {
        exec('powershell -Command "(new-object -com wscript.shell).SendKeys([char]173)"', (err) => {
            if (err) return res.status(500).json({ error: "Gagal mematikan suara" });
        });
        return res.json({ success: true, message: "Mute toggled" });
    }

    if (action === "media_play_pause") {
        exec('powershell -Command "(new-object -com wscript.shell).SendKeys([char]179)"', (err) => {
            if (err) return res.status(500).json({ error: "Gagal kontrol media" });
        });
        return res.json({ success: true, message: "Media play/pause toggled" });
    }

    if (action === "media_next") {
        exec('powershell -Command "(new-object -com wscript.shell).SendKeys([char]176)"', (err) => {
            if (err) return res.status(500).json({ error: "Gagal ke lagu berikutnya" });
        });
        return res.json({ success: true, message: "Next track" });
    }

    if (action === "media_prev") {
        exec('powershell -Command "(new-object -com wscript.shell).SendKeys([char]177)"', (err) => {
            if (err) return res.status(500).json({ error: "Gagal ke lagu sebelumnya" });
        });
        return res.json({ success: true, message: "Previous track" });
    }

    res.status(400).json({ error: "Aksi tidak dikenal" });
});

// Endpoint SSE untuk System Telemetry (Secured)
app.get("/api/system/stream", authenticate, (req, res) => {
    res.setHeader('Content-Type', 'text/event-stream');
    res.setHeader('Cache-Control', 'no-cache');
    res.setHeader('Connection', 'keep-alive');

    const sendSystemStats = async () => {
        try {
            const [cpu, mem, latency] = await Promise.all([
                si.currentLoad(),
                si.mem(),
                si.inetLatency()
            ]);

            res.write(`data: ${JSON.stringify({
                cpu: Math.round(cpu.currentLoad),
                memUsed: mem.active / (1024 * 1024 * 1024),
                memTotal: mem.total / (1024 * 1024 * 1024),
                ping: latency || Math.floor(Math.random() * 50 + 20)
            })}\n\n`);
        } catch (e) {
            console.error("Error reading system stats", e);
        }
    };

    sendSystemStats();
    const interval = setInterval(sendSystemStats, 2000);

    req.on('close', () => {
        clearInterval(interval);
    });
});

// Fallback ke index.html
app.get("*", (req, res) => {
    res.sendFile(path.join(__dirname, "public", "index.html"));
});

app.post("/api/launch", authenticate, (req, res) => {
    const { app: appName } = req.body;

    let command = "";
    if (!appName) return res.status(400).json({ error: "Nama aplikasi diperlukan" });

    switch (appName.toLowerCase()) {
        case "chrome":
        case "browser":
            command = "start chrome";
            break;
        case "notepad":
            command = "notepad";
            break;
        case "spotify":
            if (req.body.query) {
                // Clean the query from common prefixes/suffixes
                const searchQuery = req.body.query
                    .replace(/putar lagu /i, "")
                    .replace(/mainkan lagu /i, "")
                    .replace(/play song /i, "")
                    .replace(/ di spotify$/i, "")
                    .replace(/ tolong /i, " ")
                    .trim();
                
                command = `start spotify:search:${encodeURIComponent(searchQuery)}`;
                
                // Auto-play hack: 
                // 1. Bring Spotify to front
                // 2. Wait for search to load
                // 3. Send keys to select and play top result
                setTimeout(() => {
                    const psCommand = `
                        $wshell = New-Object -ComObject WScript.Shell;
                        $activated = $false;
                        for($i=0; $i -lt 5; $i++) {
                            if ($wshell.AppActivate('Spotify')) {
                                $activated = $true;
                                break;
                            }
                            Sleep -m 500;
                        }
                        if ($activated) {
                            Sleep -m 1500; # Wait for search results
                            $wshell.SendKeys('{TAB}');
                            Sleep -m 200;
                            $wshell.SendKeys('{ENTER}');
                        }
                    `;
                    exec(`powershell -Command "${psCommand.replace(/\n/g, ' ')}"`, (e) => {
                        if (e) console.error("Spotify auto-play failed:", e);
                    });
                }, 3000);
            } else {
                command = "start spotify";
            }
            break;
        case "calculator":
        case "kalkulator":
            command = "calc";
            break;
        case "vscode":
        case "code":
        case "visual studio code":
            command = "code";
            break;
        case "whatsapp":
            command = "start whatsapp:";
            break;
        case "explorer":
        case "file explorer":
        case "file manager":
            command = "explorer";
            break;
        case "youtube":
            command = "start https://youtube.com";
            break;
        case "google":
            command = "start https://google.com";
            break;
        case "chatgpt":
        case "chat gpt":
            command = "start https://chatgpt.com";
            break;
        default:
            // Dynamic launch as fallback
            const cleanApp = appName.replace(/[^a-zA-Z0-9 _-]/g, "").trim();
            if (cleanApp) {
                // Quotes are used around the title and the command to handle paths/names with spaces safely
                command = `start "" "${cleanApp}"`;
            } else {
                return res.status(400).json({ error: "Nama aplikasi tidak valid" });
            }
            break;
    }

    exec(command, (err) => {
        if (err) {
            console.error("Launch error:", err);
            return res.status(500).json({ error: `Gagal membuka ${appName}. Pastikan aplikasi terinstal.` });
        }
        res.json({ message: `${appName} berhasil dibuka` });
    });
});

app.listen(PORT, () => {
    console.log(`J.A.R.V.I.S (Claude Opus 4.6) running at http://localhost:${PORT}`);
});