const express = require('express');
const cors = require('cors');
const path = require('path');
const seedData = require('./seed');

const app = express();
const PORT = process.env.PORT || 5000;

// Middleware
app.use(cors());
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// Serve frontend static files
app.use(express.static(path.join(__dirname, '../frontend')));

// In-memory data store (for simplicity - in production use a real database)
global.dataStore = {
  students: [],
  courses: [],
  tasks: [],
  enrollments: [],
  completions: [],
  earnings: []
};

// Load seed data
seedData();

// Routes
app.use('/api/auth', require('./routes/auth'));
app.use('/api/students', require('./routes/students'));
app.use('/api/courses', require('./routes/courses'));
app.use('/api/tasks', require('./routes/tasks'));
app.use('/api/earnings', require('./routes/earnings'));

// Health check
app.get('/api/health', (req, res) => {
  res.json({ status: 'ok', message: 'Learn-to-Earn API is running' });
});

// Error handling middleware
app.use((err, req, res, next) => {
  console.error(err.stack);
  res.status(500).json({ error: 'Something went wrong!' });
});

// Serve frontend for any other routes
app.get('*', (req, res) => {
  if (!req.path.startsWith('/api')) {
    res.sendFile(path.join(__dirname, '../frontend/index.html'));
  } else {
    res.status(404).json({ error: 'API endpoint not found' });
  }
});

app.listen(PORT, () => {
  console.log(`Server is running on port ${PORT}`);
  console.log(`Frontend available at: http://localhost:${PORT}`);
  console.log(`API available at: http://localhost:${PORT}/api`);
});

module.exports = app;
