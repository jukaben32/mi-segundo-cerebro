const express = require('express');
const { spawn } = require('child_process');
const bodyParser = require('body-parser');
const path = require('path');
const fs = require('fs');
const app = express();
const port = 4060;

app.use(bodyParser.json());
app.use(express.static('.'));

const AUTOCLAW_DIR = path.join('C:', 'Users', 'IA Power Engine', '.gemini', 'antigravity', 'scratch', 'MisProyectos', 'autoclaw');
const AUTOCLAW_PATH = path.join(AUTOCLAW_DIR, 'dist', 'index.js');
const HISTORY_FILE = path.join(__dirname, 'history.json');

app.post('/api/chat', (req, res) => {
    const { prompt } = req.body;
    if (!prompt) return res.status(400).json({ error: 'Misión requerida' });

    console.log(`Lanzando misión: ${prompt}`);
    
    // SOLUCIÓN V8: Usamos spawn nativo de node para evitar errores de shell de Windows
    const nodePath = process.execPath;
    const processInstance = spawn(nodePath, [AUTOCLAW_PATH, prompt, "--no-interactive", "--yes"], { 
        cwd: AUTOCLAW_DIR, 
        env: { ...process.env },
        shell: false 
    });

    let stdout = '';
    processInstance.stdout.on('data', (data) => { stdout += data.toString(); });
    
    processInstance.on('close', (code) => {
        const result = stdout || 'Misión completada.';
        try {
            const currentHistory = JSON.parse(fs.readFileSync(HISTORY_FILE, 'utf-8') || '[]');
            const entry = { prompt, date: new Date().toLocaleString(), output: result.slice(0, 1000) };
            fs.writeFileSync(HISTORY_FILE, JSON.stringify([entry, ...currentHistory.slice(0, 9)], null, 2));
        } catch(e) {}
        res.json({ output: result });
    });
});

app.get('/api/files', (req, res) => {
    try {
        const files = fs.readdirSync(AUTOCLAW_DIR)
            .filter(file => ['.txt', '.md', '.json'].includes(path.extname(file)))
            .map(file => ({ name: file, date: fs.statSync(path.join(AUTOCLAW_DIR, file)).mtime.toLocaleString() }));
        res.json(files);
    } catch(e) { res.json([]); }
});

app.get('/api/history', (req, res) => {
    try { res.json(JSON.parse(fs.readFileSync(HISTORY_FILE, 'utf-8'))); } catch(e) { res.json([]); }
});

app.listen(port, () => {
    console.log(`🚀 Hub Pro v8 en http://localhost:${port}`);
    if (!fs.existsSync(HISTORY_FILE)) fs.writeFileSync(HISTORY_FILE, '[]');
});
