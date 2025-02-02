const express = require('express');
const app = express();
const path = require('path');
const jwt = require('jsonwebtoken');

function authenticateToken(req, res, next) {
    const token = req.headers['authorization']?.split(' ')[1];
    if (!token) {
        return res.redirect('/login'); // If no token, redirect to login
    }
    jwt.verify(token, 'your-secret-key', (err, user) => {
        if (err) {
            return res.redirect('/login'); // Invalid token, redirect to login
        }
        req.user = user; 
        next();
    });
}


// Serve static files in the "public" directory
app.use(express.static(path.join(__dirname, 'public')));

app.get('/protected', authenticateToken, (req, res) => {
    res.sendFile(path.join(__dirname, 'public', 'index.html'));
});

app.get('/login', (req, res) => {
    res.sendFile(path.join(__dirname, 'public', 'login.html'));
})

// Default route
app.get('/', authenticateToken, (req, res) => {
    res.sendFile(path.join(__dirname, 'public', 'index.html'));
});

const PORT = 3000;
app.listen(PORT, () => {
    console.log(`Server running on http://localhost:${PORT}`);
});
