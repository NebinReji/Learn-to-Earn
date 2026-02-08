class Task {
  constructor(id, title, description, courseId, experienceReward, moneyReward, difficulty) {
    this.id = id;
    this.title = title;
    this.description = description;
    this.courseId = courseId;
    this.experienceReward = experienceReward;
    this.moneyReward = moneyReward;
    this.difficulty = difficulty;
    this.createdAt = new Date();
  }
}

module.exports = Task;
