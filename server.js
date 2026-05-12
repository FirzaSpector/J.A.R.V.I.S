const express = require("express");
const cors = require("cors");
const path = require("path");

require("dotenv").config();

const app = express();
const PORT = process.env.PORT || 3000;

app.use(cors());
app.use(express.json());

// Serve frontend static files
app.use(express.static(path.join(__dirname, "public")));

// Proxy endpoint ke Google Gemini API
app.post("/api/chat", async (req, res) => {
    const { messages, system } = req.body;

    if (!messages || !Array.isArray(messages)) {
        return res.status(400).json({ error: "Field 'messages' harus berupa array." });
    }

    const apiKey = process.env.GEMINI_API_KEY;
    if (!apiKey) {
        return res.status(500).json({ error: "GEMINI_API_KEY belum diset di .env" });
    }

    try {
        // Convert format messages ke Gemini style
        const geminiContents = messages.map((msg) => ({
            role: msg.role === "assistant" ? "model" : "user",
            parts: [{ text: msg.content }],
        }));

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
        res.json({ reply });

    } catch (err) {
        console.error("Server error:", err);
        res.status(500).json({ error: "Internal server error: " + err.message });
    }
});

// Proxy endpoint ke Google Gemini API (STREAMING)
app.post("/api/chat/stream", async (req, res) => {
    const { messages, system } = req.body;

    if (!messages || !Array.isArray(messages)) {
        return res.status(400).json({ error: "Field 'messages' harus berupa array." });
    }

    const apiKey = process.env.GEMINI_API_KEY;
    if (!apiKey) {
        return res.status(500).json({ error: "GEMINI_API_KEY belum diset di .env" });
    }

    try {
        const geminiContents = messages.map((msg) => ({
            role: msg.role === "assistant" ? "model" : "user",
            parts: [{ text: msg.content }],
        }));

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

        const model = process.env.GEMINI_MODEL || "gemini-3.1-flash-lite";
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

// Fallback ke index.html
app.get("*", (req, res) => {
    res.sendFile(path.join(__dirname, "public", "index.html"));
});

app.listen(PORT, () => {
    console.log(`J.A.R.V.I.S (Gemini 3.1 Flash-lite) running at http://localhost:${PORT}`);
});