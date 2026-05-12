const http = require('http');
const data = JSON.stringify({
    messages: [{ role: 'user', content: 'Halo, tes singkat' }],
    system: 'Jawab dalam 1 kalimat saja.'
});
const req = http.request({
    hostname: 'localhost', port: 3000, path: '/api/chat',
    method: 'POST', headers: { 'Content-Type': 'application/json', 'Content-Length': Buffer.byteLength(data) }
}, (res) => {
    let body = '';
    res.on('data', c => body += c);
    res.on('end', () => console.log('STATUS:', res.statusCode, '\nRESPONSE:', body));
});
req.on('error', e => console.error('ERROR:', e.message));
req.write(data);
req.end();
