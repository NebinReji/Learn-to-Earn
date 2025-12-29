class Student {
  constructor(id, name, email, password) {
    this.id = id;
    this.name = name;
    this.email = email;
    this.password = password;
    this.experiencePoints = 0;
    this.totalEarnings = 0;
    this.skills = [];
    this.badges = [];
    this.createdAt = new Date();
  }

  addExperience(points) {
    this.experiencePoints += points;
  }

  addEarnings(amount) {
    this.totalEarnings += amount;
  }

  addSkill(skill) {
    if (!this.skills.includes(skill)) {
      this.skills.push(skill);
    }
  }

  addBadge(badge) {
    this.badges.push({
      name: badge,
      earnedAt: new Date()
    });
  }

  getLevel() {
    return Math.floor(this.experiencePoints / 100) + 1;
  }
}

module.exports = Student;
