const express = require('express');
const router = express.Router();

// Get all tasks
router.get('/', (req, res) => {
  const { courseId, difficulty } = req.query;
  let tasks = global.dataStore.tasks;

  if (courseId) {
    tasks = tasks.filter(t => t.courseId === courseId);
  }

  if (difficulty) {
    tasks = tasks.filter(t => t.difficulty === difficulty);
  }

  res.json(tasks);
});

// Get single task
router.get('/:id', (req, res) => {
  const task = global.dataStore.tasks.find(t => t.id === req.params.id);

  if (!task) {
    return res.status(404).json({ error: 'Task not found' });
  }

  res.json(task);
});

// Complete a task
router.post('/:id/complete', (req, res) => {
  const { studentId } = req.body;
  const task = global.dataStore.tasks.find(t => t.id === req.params.id);
  const student = global.dataStore.students.find(s => s.id === studentId);

  if (!task || !student) {
    return res.status(404).json({ error: 'Task or student not found' });
  }

  const alreadyCompleted = global.dataStore.completions.find(
    c => c.studentId === studentId && c.taskId === task.id && c.type === 'task'
  );

  if (alreadyCompleted) {
    return res.status(400).json({ error: 'Task already completed' });
  }

  // Add experience points and earnings
  student.addExperience(task.experienceReward);
  student.addEarnings(task.moneyReward);

  // Record earnings
  global.dataStore.earnings.push({
    id: Date.now().toString(),
    studentId,
    taskId: task.id,
    amount: task.moneyReward,
    earnedAt: new Date()
  });

  // Record completion
  global.dataStore.completions.push({
    id: Date.now().toString(),
    studentId,
    taskId: task.id,
    type: 'task',
    completedAt: new Date()
  });

  // Award badges for task milestones
  const completedTasks = global.dataStore.completions.filter(
    c => c.studentId === studentId && c.type === 'task'
  ).length;

  if (completedTasks === 1) {
    student.addBadge('First Task Completed');
  } else if (completedTasks === 10) {
    student.addBadge('Task Warrior');
  } else if (completedTasks === 50) {
    student.addBadge('Task Master');
  }

  // Award badges for earnings milestones
  if (student.totalEarnings >= 100 && student.totalEarnings - task.moneyReward < 100) {
    student.addBadge('First $100 Earned');
  } else if (student.totalEarnings >= 500 && student.totalEarnings - task.moneyReward < 500) {
    student.addBadge('Earning Expert');
  }

  res.json({
    message: 'Task completed successfully',
    experienceGained: task.experienceReward,
    moneyEarned: task.moneyReward,
    newLevel: student.getLevel(),
    totalEarnings: student.totalEarnings
  });
});

module.exports = router;
