const Course = require('./models/Course');
const Task = require('./models/Task');

function seedData() {
  // Create sample courses
  const webDevCourse = new Course(
    '1',
    'Web Development Fundamentals',
    'Learn the basics of HTML, CSS, and JavaScript',
    'Web Development',
    'beginner',
    100
  );
  webDevCourse.addSkill('HTML');
  webDevCourse.addSkill('CSS');
  webDevCourse.addSkill('JavaScript');

  const pythonCourse = new Course(
    '2',
    'Python Programming',
    'Master Python from basics to advanced concepts',
    'Programming',
    'beginner',
    120
  );
  pythonCourse.addSkill('Python');
  pythonCourse.addSkill('Programming Logic');

  const dataScienceCourse = new Course(
    '3',
    'Data Science with Python',
    'Learn data analysis and visualization with Python',
    'Data Science',
    'intermediate',
    150
  );
  dataScienceCourse.addSkill('Python');
  dataScienceCourse.addSkill('Data Analysis');
  dataScienceCourse.addSkill('Pandas');
  dataScienceCourse.addSkill('NumPy');

  const reactCourse = new Course(
    '4',
    'React for Beginners',
    'Build modern web applications with React',
    'Web Development',
    'intermediate',
    140
  );
  reactCourse.addSkill('React');
  reactCourse.addSkill('JavaScript');
  reactCourse.addSkill('Frontend Development');

  const mlCourse = new Course(
    '5',
    'Machine Learning Basics',
    'Introduction to Machine Learning concepts',
    'Artificial Intelligence',
    'advanced',
    200
  );
  mlCourse.addSkill('Machine Learning');
  mlCourse.addSkill('Python');
  mlCourse.addSkill('scikit-learn');

  global.dataStore.courses = [
    webDevCourse,
    pythonCourse,
    dataScienceCourse,
    reactCourse,
    mlCourse
  ];

  // Create sample tasks
  global.dataStore.tasks = [
    // Web Development Tasks
    new Task('1', 'Build a Personal Portfolio', 'Create a portfolio website using HTML, CSS, and JavaScript', '1', 50, 25, 'beginner'),
    new Task('2', 'Create a Responsive Landing Page', 'Design a mobile-responsive landing page', '1', 40, 20, 'beginner'),
    new Task('3', 'Build a Todo App', 'Create an interactive todo application', '1', 60, 30, 'intermediate'),
    
    // Python Tasks
    new Task('4', 'Build a Calculator', 'Create a command-line calculator in Python', '2', 30, 15, 'beginner'),
    new Task('5', 'Create a Weather App', 'Build a weather app using Python and APIs', '2', 50, 25, 'intermediate'),
    new Task('6', 'Data Scraper Project', 'Create a web scraper using BeautifulSoup', '2', 70, 35, 'intermediate'),
    
    // Data Science Tasks
    new Task('7', 'Analyze Sales Data', 'Perform data analysis on sales dataset', '3', 60, 30, 'intermediate'),
    new Task('8', 'Create Data Visualizations', 'Build interactive charts and graphs', '3', 55, 28, 'intermediate'),
    new Task('9', 'Predictive Analysis Project', 'Build a predictive model for business data', '3', 80, 40, 'advanced'),
    
    // React Tasks
    new Task('10', 'Build a Blog with React', 'Create a blog application using React', '4', 70, 35, 'intermediate'),
    new Task('11', 'E-commerce Product Page', 'Build a product listing page with cart', '4', 65, 32, 'intermediate'),
    new Task('12', 'Social Media Dashboard', 'Create a dashboard with React hooks', '4', 75, 38, 'advanced'),
    
    // Machine Learning Tasks
    new Task('13', 'Image Classification Model', 'Build an image classifier', '5', 100, 50, 'advanced'),
    new Task('14', 'Sentiment Analysis Tool', 'Create a sentiment analysis application', '5', 90, 45, 'advanced'),
    new Task('15', 'Recommendation System', 'Build a basic recommendation engine', '5', 110, 55, 'advanced')
  ];

  console.log('Seed data loaded successfully!');
  console.log(`- ${global.dataStore.courses.length} courses`);
  console.log(`- ${global.dataStore.tasks.length} tasks`);
}

module.exports = seedData;
