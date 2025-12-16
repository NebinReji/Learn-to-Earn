const express = require('express');
const router = express.Router();

// Get student profile
router.get('/:id', (req, res) => {
  const student = global.dataStore.students.find(s => s.id === req.params.id);

  if (!student) {
    return res.status(404).json({ error: 'Student not found' });
  }

  res.json({
    id: student.id,
    name: student.name,
    email: student.email,
    experiencePoints: student.experiencePoints,
    totalEarnings: student.totalEarnings,
    level: student.getLevel(),
    skills: student.skills,
    badges: student.badges,
    createdAt: student.createdAt
  });
});

// Get student dashboard stats
router.get('/:id/dashboard', (req, res) => {
  const student = global.dataStore.students.find(s => s.id === req.params.id);

  if (!student) {
    return res.status(404).json({ error: 'Student not found' });
  }

  const enrollments = global.dataStore.enrollments.filter(e => e.studentId === req.params.id);
  const completions = global.dataStore.completions.filter(c => c.studentId === req.params.id);

  res.json({
    profile: {
      name: student.name,
      level: student.getLevel(),
      experiencePoints: student.experiencePoints,
      totalEarnings: student.totalEarnings
    },
    stats: {
      coursesEnrolled: enrollments.length,
      coursesCompleted: completions.filter(c => c.type === 'course').length,
      tasksCompleted: completions.filter(c => c.type === 'task').length,
      skillsAcquired: student.skills.length,
      badgesEarned: student.badges.length
    },
    recentActivity: completions.slice(-5).reverse()
  });
});

// Get leaderboard
router.get('/', (req, res) => {
  const leaderboard = global.dataStore.students
    .map(s => ({
      id: s.id,
      name: s.name,
      experiencePoints: s.experiencePoints,
      totalEarnings: s.totalEarnings,
      level: s.getLevel(),
      badges: s.badges.length
    }))
    .sort((a, b) => b.experiencePoints - a.experiencePoints)
    .slice(0, 10);

  res.json(leaderboard);
});

module.exports = router;
