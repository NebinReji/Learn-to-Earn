const express = require('express');
const router = express.Router();
const Student = require('../models/Student');

// Simple authentication (in production, use proper auth with JWT, bcrypt, etc.)
router.post('/register', (req, res) => {
  const { name, email, password } = req.body;

  if (!name || !email || !password) {
    return res.status(400).json({ error: 'All fields are required' });
  }

  // Check if student already exists
  const existingStudent = global.dataStore.students.find(s => s.email === email);
  if (existingStudent) {
    return res.status(400).json({ error: 'Email already registered' });
  }

  const student = new Student(
    Date.now().toString(),
    name,
    email,
    password // In production, hash this!
  );

  global.dataStore.students.push(student);

  res.status(201).json({
    message: 'Student registered successfully',
    student: {
      id: student.id,
      name: student.name,
      email: student.email,
      experiencePoints: student.experiencePoints,
      totalEarnings: student.totalEarnings
    }
  });
});

router.post('/login', (req, res) => {
  const { email, password } = req.body;

  if (!email || !password) {
    return res.status(400).json({ error: 'Email and password are required' });
  }

  const student = global.dataStore.students.find(
    s => s.email === email && s.password === password
  );

  if (!student) {
    return res.status(401).json({ error: 'Invalid credentials' });
  }

  res.json({
    message: 'Login successful',
    student: {
      id: student.id,
      name: student.name,
      email: student.email,
      experiencePoints: student.experiencePoints,
      totalEarnings: student.totalEarnings,
      level: student.getLevel(),
      skills: student.skills,
      badges: student.badges
    }
  });
});

module.exports = router;
