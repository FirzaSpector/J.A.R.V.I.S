require("dotenv").config();

async function listModels() {
    const apiKey = process.env.GEMINI_API_KEY;
    const url = `https://generativelanguage.googleapis.com/v1beta/models?key=${apiKey}`;

    try {
        const response = await fetch(url);
        const data = await response.json();
        
        if (data.models) {
            console.log("Model yang tersedia untuk API Key kamu:");
            data.models.forEach(m => {
                if (m.supportedGenerationMethods.includes("generateContent")) {
                    console.log("- " + m.name.replace("models/", ""));
                }
            });
        } else {
            console.log("Gagal mengambil data:", data);
        }
    } catch (err) {
        console.error("Error:", err.message);
    }
}

listModels();
