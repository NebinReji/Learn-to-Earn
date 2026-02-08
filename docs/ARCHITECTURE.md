# Architecture Overview

## System Architecture

Learn to Earn follows a client-server architecture with a RESTful API backend and a web-based frontend.

```
┌─────────────────┐
│   Frontend      │
│  (HTML/JS/CSS)  │
└────────┬────────┘
         │ HTTP/REST
         ▼
┌─────────────────┐
│   Express.js    │
│   Backend API   │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   In-Memory     │
│   Data Store    │
└─────────────────┘
```

## Components

### Backend (Node.js + Express)

#### Models
- **Student**: Represents a user in the system
  - Properties: id, name, email, password, experiencePoints, totalEarnings, skills, badges
  - Methods: addExperience(), addEarnings(), addSkill(), addBadge(), getLevel()

- **Course**: Represents a learning course
  - Properties: id, title, description, category, difficulty, experienceReward, skills

- **Task**: Represents a project/task that students can complete
  - Properties: id, title, description, courseId, experienceReward, moneyReward, difficulty

#### Routes
- **/api/auth**: Authentication endpoints (register, login)
- **/api/students**: Student profile and dashboard endpoints
- **/api/courses**: Course catalog and enrollment endpoints
- **/api/tasks**: Task listing and completion endpoints
- **/api/earnings**: Earnings history endpoints

#### Data Store
Currently uses an in-memory global data store with the following collections:
- students
- courses
- tasks
- enrollments
- completions
- earnings

**Note**: In production, this should be replaced with a proper database (MongoDB, PostgreSQL, etc.)

### Frontend (HTML/CSS/JavaScript)

#### Pages/Views
- **Authentication View**: Registration and login forms
- **Dashboard View**: Main student interface with tabs for:
  - Courses
  - Tasks
  - Leaderboard

#### Features
- Single Page Application (SPA) behavior
- Local storage for session persistence
- Responsive design
- Real-time updates

## Data Flow

### Student Registration/Login
```
User → Frontend Form → POST /api/auth/register → Create Student → Return Student Data
User → Frontend Form → POST /api/auth/login → Validate Credentials → Return Student Data
```

### Course Enrollment & Completion
```
Student → Click Enroll → POST /api/courses/:id/enroll → Create Enrollment Record
Student → Click Complete → POST /api/courses/:id/complete → 
    - Award Experience Points
    - Add Skills to Student
    - Create Completion Record
    - Check for Badge Awards
```

### Task Completion
```
Student → Click Complete Task → POST /api/tasks/:id/complete →
    - Award Experience Points
    - Award Money
    - Update Student Earnings
    - Create Earnings Record
    - Create Completion Record
    - Check for Badge Awards
```

## Gamification System

### Experience & Levels
- Students start at Level 1 with 0 XP
- Every 100 XP earned = 1 level increase
- XP is awarded for:
  - Completing courses (50-200 XP depending on difficulty)
  - Completing tasks (30-110 XP depending on difficulty)

### Earning System
- Money is awarded only for completing tasks
- Task rewards range from $15 to $55
- Total earnings are tracked and displayed on the dashboard

### Badge System
- Automatic badge awards based on milestones:
  - Course milestones (1st, 5th, 10th course)
  - Task milestones (1st, 10th, 50th task)
  - Earning milestones ($100, $500)

## Security Considerations

**Current Implementation** (Development/Demo):
- Plain text password storage
- No authentication tokens
- No input validation
- CORS enabled for all origins

**Production Recommendations**:
- Use bcrypt for password hashing
- Implement JWT tokens for authentication
- Add input validation and sanitization
- Configure CORS for specific origins
- Add rate limiting
- Use HTTPS
- Implement proper session management
- Add SQL injection protection (if using SQL database)
- Add XSS protection

## Scalability Considerations

### Current Limitations
- In-memory storage (data lost on restart)
- Single server instance
- No caching layer
- No load balancing

### Production Improvements
- Database integration (MongoDB/PostgreSQL)
- Redis for caching and sessions
- Horizontal scaling with load balancer
- CDN for static assets
- Microservices architecture for different features
- Message queue for async tasks
- Monitoring and logging system

## Technology Stack

- **Backend**: Node.js, Express.js
- **Frontend**: HTML5, CSS3, Vanilla JavaScript
- **Data Storage**: In-memory (planned: MongoDB/PostgreSQL)
- **Development**: nodemon for auto-reload

## API Design Principles

- RESTful architecture
- JSON for data exchange
- Stateless server design
- Clear HTTP status codes
- Consistent error handling
- Descriptive endpoint naming
