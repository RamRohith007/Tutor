from django.db import models  # Ensure models is imported for new classes
from django.contrib.auth.models import AbstractUser
# --- Faculty, Logistics, and Enrollment Fee Models ---
class Faculty(models.Model):
	name = models.CharField(max_length=100)
	initials = models.CharField(max_length=4, help_text="Short initials, e.g. PR")
	title = models.CharField(max_length=100)
	bio = models.TextField()
	linkedin = models.URLField(blank=True)
	skills = models.CharField(max_length=300, help_text="Comma-separated skills")

	def skill_list(self):
		return [s.strip() for s in self.skills.split(',') if s.strip()]

	def __str__(self):
		return self.name


class LogisticsSession(models.Model):
	title = models.CharField(max_length=100)
	description = models.TextField()
	order = models.PositiveIntegerField(default=1)

	class Meta:
		ordering = ['order']

	def __str__(self):
		return self.title


class EnrollmentFee(models.Model):
	currency_inr = models.PositiveIntegerField(default=50000)
	currency_usd = models.PositiveIntegerField(default=600)
	details = models.TextField(help_text="Comma-separated features, e.g. 1-on-1 GenAI Expert Mentorship, 8 Graded Production Assignments")

	def detail_list(self):
		return [d.strip() for d in self.details.split(',') if d.strip()]

	def __str__(self):
		return f"Fee: ₹{self.currency_inr} / ${self.currency_usd}"


class CourseBatch(models.Model):
	name = models.CharField(max_length=200, help_text="Batch or cohort name, e.g. Fall 2026")
	start_date = models.DateField()
	end_date = models.DateField()
	description = models.TextField(blank=True)
	capacity = models.PositiveIntegerField(null=True, blank=True, help_text="Optional capacity for the batch")
	is_active = models.BooleanField(default=True)
	faculty = models.ForeignKey(
		Faculty,
		null=True,
		blank=True,
		on_delete=models.SET_NULL,
		related_name='batches',
		help_text="Faculty member leading this batch"
	)

	class Meta:
		ordering = ['start_date']

	def __str__(self):
		return f"{self.name} ({self.start_date} – {self.end_date})"


class User(AbstractUser):
	USER_TYPE_CHOICES = (
		('admin', 'Admin'),
		('staff', 'Staff'),
		('student', 'Student'),
		('user', 'User'),
	)
	user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES, default='user')
	active = models.BooleanField(default=True)
	current_role = models.CharField(max_length=150, blank=True, help_text="Current professional role or job title")
	mobile_number = models.CharField(max_length=25, blank=True, help_text="Mobile number for the user")
	enrolled_batch = models.ForeignKey(
		'CourseBatch',
		null=True,
		blank=True,
		on_delete=models.SET_NULL,
		related_name='students',
	)
	faculty = models.ForeignKey(
		Faculty,
		null=True,
		blank=True,
		on_delete=models.SET_NULL,
		related_name='staff_members',
	)


class Note(models.Model):
	title = models.CharField(max_length=200)
	content = models.TextField()
	batch = models.ForeignKey(CourseBatch, on_delete=models.CASCADE, related_name='notes')
	created_by = models.ForeignKey(User, on_delete=models.CASCADE)
	created_at = models.DateTimeField(auto_now_add=True)

	class Meta:
		ordering = ['-created_at']

	def __str__(self):
		return f"{self.title} ({self.batch.name})"


class Recording(models.Model):
	title = models.CharField(max_length=200)
	url = models.URLField(help_text="Link to the recording")
	batch = models.ForeignKey(CourseBatch, on_delete=models.CASCADE, related_name='recordings')
	created_by = models.ForeignKey(User, on_delete=models.CASCADE)
	created_at = models.DateTimeField(auto_now_add=True)

	class Meta:
		ordering = ['-created_at']

	def __str__(self):
		return f"{self.title} ({self.batch.name})"


# Admissions model
class Admission(models.Model):
	full_name = models.CharField(max_length=100)
	email = models.EmailField()
	motivation = models.TextField()
	submitted_at = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return f"{self.full_name} ({self.email})"

# Curriculum Phase and Assignment models
class Phase(models.Model):
	name = models.CharField(max_length=100)
	description = models.TextField(blank=True)

	def __str__(self):
		return self.name

class Assignment(models.Model):
	phase = models.ForeignKey(Phase, on_delete=models.CASCADE, related_name='assignments')
	batch = models.ForeignKey(CourseBatch, null=True, blank=True, on_delete=models.CASCADE, related_name='assignments')
	title = models.CharField(max_length=200)
	description = models.TextField(blank=True)
	due_date = models.DateField(null=True, blank=True)

	def __str__(self):
		return f"{self.title} ({self.batch.name if self.batch else self.phase.name})"


# --- Dynamic Curriculum & Practicum Models ---
class CurriculumPhase(models.Model):
	title = models.CharField(max_length=200)
	order = models.PositiveIntegerField(default=1)
	description = models.TextField(blank=True)

	class Meta:
		ordering = ['order']

	def __str__(self):
		return f"Phase {self.order:02d}: {self.title}"


class CurriculumSection(models.Model):
	phase = models.ForeignKey(CurriculumPhase, related_name='sections', on_delete=models.CASCADE)
	name = models.CharField(max_length=200)
	order = models.PositiveIntegerField(default=1)
	topics = models.TextField(help_text="Comma-separated list of topics")

	class Meta:
		ordering = ['order']

	def topic_list(self):
		return [t.strip() for t in self.topics.split(',') if t.strip()]

	def __str__(self):
		return f"{self.phase} - {self.name}"


class PracticumProject(models.Model):
	title = models.CharField(max_length=200)
	order = models.PositiveIntegerField(default=1)
	icon = models.CharField(max_length=10, default="🔍", help_text="Emoji or icon")
	description = models.TextField()
	tags = models.CharField(max_length=200, help_text="Comma-separated tags")

	class Meta:
		ordering = ['order']

	def tag_list(self):
		return [t.strip() for t in self.tags.split(',') if t.strip()]

	def __str__(self):
		return self.title


class PracticumVertical(models.Model):
	name = models.CharField(max_length=200)
	order = models.PositiveIntegerField(default=1)

	class Meta:
		ordering = ['order']

	def __str__(self):
		return self.name
