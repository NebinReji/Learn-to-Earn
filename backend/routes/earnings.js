const express = require('express');
const router = express.Router();

// Get student earnings
router.get('/:studentId', (req, res) => {
  const student = global.dataStore.students.find(s => s.id === req.params.studentId);

  if (!student) {
    return res.status(404).json({ error: 'Student not found' });
  }

  const earnings = global.dataStore.earnings.filter(e => e.studentId === req.params.studentId);

  res.json({
    totalEarnings: student.totalEarnings,
    earningsHistory: earnings.map(e => {
      const task = global.dataStore.tasks.find(t => t.id === e.taskId);
      return {
        id: e.id,
        amount: e.amount,
        taskTitle: task ? task.title : 'Unknown',
        earnedAt: e.earnedAt
      };
    })
  });
});

module.exports = router;
