const express = require('express');
const router = express.Router();
const Course = require('../models/Course');

// Get all courses
router.get('/', (req, res) => {
  const { category, difficulty } = req.query;
  let courses = global.dataStore.courses;

  if (category) {
    courses = courses.filter(c => c.category === category);
  }

  if (difficulty) {
    courses = courses.filter(c => c.difficulty === difficulty);
  }

  res.json(courses);
});

// Get single course
router.get('/:id', (req, res) => {
  const course = global.dataStore.courses.find(c => c.id === req.params.id);

  if (!course) {
    return res.status(404).json({ error: 'Course not found' });
  }

  const tasks = global.dataStore.tasks.filter(t => t.courseId === course.id);

  res.json({
    ...course,
    tasks
  });
});

// Enroll in a course
router.post('/:id/enroll', (req, res) => {
  const { studentId } = req.body;
  const course = global.dataStore.courses.find(c => c.id === req.params.id);
  const student = global.dataStore.students.find(s => s.id === studentId);

  if (!course) {
    return res.status(404).json({ error: 'Course not found' });
  }

  if (!student) {
    return res.status(404).json({ error: 'Student not found' });
  }

  const alreadyEnrolled = global.dataStore.enrollments.find(
    e => e.studentId === studentId && e.courseId === course.id
  );

  if (alreadyEnrolled) {
    return res.status(400).json({ error: 'Already enrolled in this course' });
  }

  global.dataStore.enrollments.push({
    id: Date.now().toString(),
    studentId,
    courseId: course.id,
    enrolledAt: new Date()
  });

  res.json({ message: 'Enrolled successfully', course });
});

// Complete a course
router.post('/:id/complete', (req, res) => {
  const { studentId } = req.body;
  const course = global.dataStore.courses.find(c => c.id === req.params.id);
  const student = global.dataStore.students.find(s => s.id === studentId);

  if (!course || !student) {
    return res.status(404).json({ error: 'Course or student not found' });
  }

  const enrollment = global.dataStore.enrollments.find(
    e => e.studentId === studentId && e.courseId === course.id
  );

  if (!enrollment) {
    return res.status(400).json({ error: 'Not enrolled in this course' });
  }

  const alreadyCompleted = global.dataStore.completions.find(
    c => c.studentId === studentId && c.courseId === course.id && c.type === 'course'
  );

  if (alreadyCompleted) {
    return res.status(400).json({ error: 'Course already completed' });
  }

  // Add experience points
  student.addExperience(course.experienceReward);

  // Add skills
  course.skills.forEach(skill => student.addSkill(skill));

  // Record completion
  global.dataStore.completions.push({
    id: Date.now().toString(),
    studentId,
    courseId: course.id,
    type: 'course',
    completedAt: new Date()
  });

  // Award badge for milestones
  const completedCourses = global.dataStore.completions.filter(
    c => c.studentId === studentId && c.type === 'course'
  ).length;

  if (completedCourses === 1) {
    student.addBadge('First Course Completed');
  } else if (completedCourses === 5) {
    student.addBadge('Course Master');
  } else if (completedCourses === 10) {
    student.addBadge('Learning Champion');
  }

  res.json({
    message: 'Course completed successfully',
    experienceGained: course.experienceReward,
    newLevel: student.getLevel(),
    skillsLearned: course.skills
  });
});

module.exports = router;
