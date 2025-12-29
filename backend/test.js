/**
 * Basic API Tests for Learn to Earn
 * 
 * These tests verify core functionality of the student ecosystem.
 * Run with: node backend/test.js (after starting the server)
 */

const http = require('http');

const API_URL = 'http://localhost:5000';
let testStudent = null;

// Helper function to make HTTP requests
function makeRequest(method, path, data = null) {
  return new Promise((resolve, reject) => {
    const url = new URL(path, API_URL);
    const options = {
      method,
      hostname: url.hostname,
      port: url.port,
      path: url.pathname + url.search,
      headers: {
        'Content-Type': 'application/json'
      }
    };

    const req = http.request(options, (res) => {
      let body = '';
      res.on('data', chunk => body += chunk);
      res.on('end', () => {
        try {
          const jsonData = JSON.parse(body);
          resolve({ status: res.statusCode, data: jsonData });
        } catch (e) {
          resolve({ status: res.statusCode, data: body });
        }
      });
    });

    req.on('error', reject);

    if (data) {
      req.write(JSON.stringify(data));
    }

    req.end();
  });
}

// Test functions
async function testHealthCheck() {
  console.log('Testing health check...');
  const result = await makeRequest('GET', '/api/health');
  if (result.status === 200 && result.data.status === 'ok') {
    console.log('✓ Health check passed');
    return true;
  } else {
    console.log('✗ Health check failed');
    return false;
  }
}

async function testRegistration() {
  console.log('\nTesting student registration...');
  const testData = {
    name: 'Test Student',
    email: `test${Date.now()}@example.com`,
    password: 'testpass123'
  };

  const result = await makeRequest('POST', '/api/auth/register', testData);
  if (result.status === 201 && result.data.student) {
    testStudent = result.data.student;
    console.log('✓ Registration successful');
    console.log(`  Student ID: ${testStudent.id}`);
    return true;
  } else {
    console.log('✗ Registration failed');
    console.log(`  Error: ${result.data.error || 'Unknown error'}`);
    return false;
  }
}

async function testCourseRetrieval() {
  console.log('\nTesting course retrieval...');
  const result = await makeRequest('GET', '/api/courses');
  if (result.status === 200 && Array.isArray(result.data)) {
    console.log('✓ Course retrieval successful');
    console.log(`  Found ${result.data.length} courses`);
    return true;
  } else {
    console.log('✗ Course retrieval failed');
    return false;
  }
}

async function testTaskRetrieval() {
  console.log('\nTesting task retrieval...');
  const result = await makeRequest('GET', '/api/tasks');
  if (result.status === 200 && Array.isArray(result.data)) {
    console.log('✓ Task retrieval successful');
    console.log(`  Found ${result.data.length} tasks`);
    return true;
  } else {
    console.log('✗ Task retrieval failed');
    return false;
  }
}

async function testCourseEnrollment() {
  console.log('\nTesting course enrollment...');
  if (!testStudent) {
    console.log('✗ No test student available');
    return false;
  }

  const result = await makeRequest('POST', '/api/courses/1/enroll', {
    studentId: testStudent.id
  });

  if (result.status === 200 && result.data.message === 'Enrolled successfully') {
    console.log('✓ Course enrollment successful');
    return true;
  } else {
    console.log('✗ Course enrollment failed');
    console.log(`  Error: ${result.data.error || 'Unknown error'}`);
    return false;
  }
}

async function testTaskCompletion() {
  console.log('\nTesting task completion...');
  if (!testStudent) {
    console.log('✗ No test student available');
    return false;
  }

  const result = await makeRequest('POST', '/api/tasks/1/complete', {
    studentId: testStudent.id
  });

  if (result.status === 200 && result.data.message === 'Task completed successfully') {
    console.log('✓ Task completion successful');
    console.log(`  Experience gained: ${result.data.experienceGained}`);
    console.log(`  Money earned: $${result.data.moneyEarned}`);
    console.log(`  New level: ${result.data.newLevel}`);
    return true;
  } else {
    console.log('✗ Task completion failed');
    console.log(`  Error: ${result.data.error || 'Unknown error'}`);
    return false;
  }
}

async function testStudentProfile() {
  console.log('\nTesting student profile retrieval...');
  if (!testStudent) {
    console.log('✗ No test student available');
    return false;
  }

  const result = await makeRequest('GET', `/api/students/${testStudent.id}`);
  if (result.status === 200 && result.data.id === testStudent.id) {
    console.log('✓ Student profile retrieval successful');
    console.log(`  Name: ${result.data.name}`);
    console.log(`  Level: ${result.data.level}`);
    console.log(`  XP: ${result.data.experiencePoints}`);
    console.log(`  Earnings: $${result.data.totalEarnings}`);
    return true;
  } else {
    console.log('✗ Student profile retrieval failed');
    return false;
  }
}

async function testLeaderboard() {
  console.log('\nTesting leaderboard...');
  const result = await makeRequest('GET', '/api/students');
  if (result.status === 200 && Array.isArray(result.data)) {
    console.log('✓ Leaderboard retrieval successful');
    console.log(`  Students on leaderboard: ${result.data.length}`);
    return true;
  } else {
    console.log('✗ Leaderboard retrieval failed');
    return false;
  }
}

// Run all tests
async function runTests() {
  console.log('========================================');
  console.log('Learn to Earn - API Test Suite');
  console.log('========================================\n');

  const tests = [
    testHealthCheck,
    testRegistration,
    testCourseRetrieval,
    testTaskRetrieval,
    testCourseEnrollment,
    testTaskCompletion,
    testStudentProfile,
    testLeaderboard
  ];

  let passed = 0;
  let failed = 0;

  for (const test of tests) {
    try {
      const result = await test();
      if (result) {
        passed++;
      } else {
        failed++;
      }
    } catch (error) {
      console.log(`✗ Test failed with error: ${error.message}`);
      failed++;
    }
  }

  console.log('\n========================================');
  console.log('Test Summary');
  console.log('========================================');
  console.log(`Total tests: ${tests.length}`);
  console.log(`Passed: ${passed}`);
  console.log(`Failed: ${failed}`);
  console.log('========================================\n');

  if (failed === 0) {
    console.log('🎉 All tests passed!');
  } else {
    console.log('⚠️  Some tests failed. Please review the output above.');
  }

  process.exit(failed === 0 ? 0 : 1);
}

// Run tests
runTests().catch(error => {
  console.error('Test suite failed:', error);
  process.exit(1);
});
