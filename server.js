const express = require('express');
const fs = require('fs');
const path = require('path');
const app = express();
const port = 3000;

app.use(express.static(path.join(__dirname, 'public')));

app.get('/api/exhibitions', (req, res) => {
  fs.readFile('./data.json', 'utf8', (err, data) => {
    if (err) {
      console.error('Σφάλμα κατά την ανάγνωση του αρχείου:', err);
      res.status(500).send('Σφάλμα στον εξυπηρετητή');
      return;
    }
    res.json(JSON.parse(data));
  });
});

app.get('/api/links', (req, res) => {
  fs.readFile('./links.json', 'utf8', (err, data) => {
    if (err) {
      console.error('Σφάλμα κατά την ανάγνωση του αρχείου συνδέσμων:', err);
      res.status(500).send('Σφάλμα στον εξυπηρετητή');
      return;
    }
    res.json(JSON.parse(data));
  });
});

app.get('/', (req, res) => {
  res.sendFile(path.join(__dirname, 'public', 'index.html'));
});

app.listen(3000, () => {
  console.log(`Server is running at http://localhost:3000`);
});