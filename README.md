# 🎓 Learn to Earn - Student Ecosystem

A comprehensive student learning platform where students can learn, earn money, and gain valuable experience to improve their lives.

## 🌟 Overview

Learn to Earn is a student-centric ecosystem that combines education with real-world earning opportunities. Students can:
- 📚 Enroll in courses to learn new skills
- 💼 Complete practical tasks and projects
- 💰 Earn money for completing tasks
- ⭐ Gain experience points and level up
- 🏆 Earn badges and achievements
- 📊 Track their progress on a personalized dashboard
- 🎯 Compete on the leaderboard

## ✨ Features

### For Students
- **User Authentication**: Secure registration and login system
- **Course Catalog**: Browse and enroll in courses across various categories
  - Web Development
  - Programming
  - Data Science
  - Artificial Intelligence
  - And more!
- **Task System**: Complete real-world projects to earn money and experience
- **Progress Tracking**: Monitor your learning journey with detailed statistics
- **Gamification**: Earn experience points, level up, and collect badges
- **Leaderboard**: See how you rank against other students
- **Skills Tracking**: Build your skill portfolio as you learn

### Technical Features
- RESTful API backend with Express.js
- In-memory data storage (easily replaceable with a database)
- Responsive web interface
- Real-time updates
- Clean and intuitive UI

## 🚀 Getting Started

### Prerequisites
- Node.js (v14 or higher)
- npm or yarn

### Installation

1. Clone the repository:
```bash
git clone https://github.com/NebinReji/Learn-to-Earn.git
cd Learn-to-Earn
```

2. Install dependencies:
```bash
npm install
```

3. Start the server:
```bash
npm start
```

For development with auto-reload:
```bash
npm run dev
```

4. Open the application:
- Open your browser and go to: http://localhost:5000
- API endpoints are available at: http://localhost:5000/api

## 📖 How to Use

### 1. Register an Account
- Open the frontend application
- Fill in your name, email, and password
- Click "Create Account"

### 2. Login
- Enter your email and password
- Click "Login"

### 3. Explore Courses
- Browse available courses in different categories
- View course details including difficulty level and experience rewards
- Enroll in courses that interest you
- Complete courses to earn experience points and skills

### 4. Complete Tasks
- Navigate to the Tasks tab
- Browse available tasks
- Complete tasks to earn both experience points AND money
- Watch your earnings grow!

### 5. Track Progress
- View your dashboard to see:
  - Your current level
  - Total experience points
  - Total earnings
  - Courses completed
  - Skills acquired
  - Badges earned

### 6. Compete
- Check the Leaderboard tab to see top students
- Work hard to climb the rankings!

## 🎮 Gamification System

### Experience Points (XP)
- Earn XP by completing courses and tasks
- Every 100 XP = 1 Level increase
- Higher difficulty tasks/courses give more XP

### Money Rewards
- Complete tasks to earn money
- Different tasks offer different monetary rewards
- Track your total earnings on your dashboard

### Badges
- **First Course Completed**: Complete your first course
- **Course Master**: Complete 5 courses
- **Learning Champion**: Complete 10 courses
- **First Task Completed**: Complete your first task
- **Task Warrior**: Complete 10 tasks
- **Task Master**: Complete 50 tasks
- **First $100 Earned**: Earn your first $100
- **Earning Expert**: Earn $500

### Difficulty Levels
- 🟢 **Beginner**: Great for those just starting out
- 🟡 **Intermediate**: For students with some experience
- 🔴 **Advanced**: Challenging projects for experienced learners

## 🛠️ API Documentation

### Authentication

#### Register
```
POST /api/auth/register
Body: { name, email, password }
```

#### Login
```
POST /api/auth/login
Body: { email, password }
```

### Students

#### Get Student Profile
```
GET /api/students/:id
```

#### Get Student Dashboard
```
GET /api/students/:id/dashboard
```

#### Get Leaderboard
```
GET /api/students
```

### Courses

#### Get All Courses
```
GET /api/courses
Query params: category, difficulty (optional)
```

#### Get Course Details
```
GET /api/courses/:id
```

#### Enroll in Course
```
POST /api/courses/:id/enroll
Body: { studentId }
```

#### Complete Course
```
POST /api/courses/:id/complete
Body: { studentId }
```

### Tasks

#### Get All Tasks
```
GET /api/tasks
Query params: courseId, difficulty (optional)
```

#### Get Task Details
```
GET /api/tasks/:id
```

#### Complete Task
```
POST /api/tasks/:id/complete
Body: { studentId }
```

### Earnings

#### Get Student Earnings
```
GET /api/earnings/:studentId
```

## 🎯 Sample Data

The system comes pre-loaded with:
- 5 courses across different categories
- 15 tasks ranging from beginner to advanced
- Various learning paths in:
  - Web Development
  - Python Programming
  - Data Science
  - React Development
  - Machine Learning

## 🔮 Future Enhancements

- Database integration (MongoDB, PostgreSQL)
- Payment processing for withdrawals
- Real-time mentorship system
- Video lessons and tutorials
- Certification system
- Social features (student networking)
- Mobile application
- AI-powered learning recommendations
- Advanced analytics dashboard
- Multi-language support

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License.

## 👨‍💻 Author

Created with ❤️ for students who want to learn and earn!

---

**Start your journey today - Learn, Earn, and Grow! 🚀**
