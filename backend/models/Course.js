class Course {
  constructor(id, title, description, category, difficulty, experienceReward) {
    this.id = id;
    this.title = title;
    this.description = description;
    this.category = category;
    this.difficulty = difficulty; // beginner, intermediate, advanced
    this.experienceReward = experienceReward;
    this.skills = [];
    this.createdAt = new Date();
  }

  addSkill(skill) {
    if (!this.skills.includes(skill)) {
      this.skills.push(skill);
    }
  }
}

module.exports = Course;
