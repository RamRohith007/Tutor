
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib.auth import get_user
from django.contrib import messages
from .models import Admission, Assignment, CourseBatch, Phase, Note, Recording


def landing(request):
	if request.user.is_authenticated:
		return redirect("dashboard")

	# Import here to avoid circular import
	from .models import CurriculumPhase, PracticumProject, Faculty, LogisticsSession, EnrollmentFee, PracticumVertical
	curriculum_phases = CurriculumPhase.objects.prefetch_related('sections').all()
	practicum_projects = PracticumProject.objects.all()
	faculty_list = Faculty.objects.all()
	logistics_sessions = LogisticsSession.objects.all()
	practicum_verticals = PracticumVertical.objects.all()
	enrollment_fee = EnrollmentFee.objects.first()
	return render(request, "core/landing.html", {
		"curriculum_phases": curriculum_phases,
		"practicum_projects": practicum_projects,
		"faculty_list": faculty_list,
		"logistics_sessions": logistics_sessions,
		"enrollment_fee": enrollment_fee,
		"practicum_verticals": practicum_verticals,
	})

@login_required(login_url="/login/")
def homepage(request):
	return redirect("dashboard")

@login_required(login_url="/login/")
def dashboard(request):
	user = request.user
	batches = []
	if user.user_type == 'staff' and user.faculty:
		batches = CourseBatch.objects.filter(faculty=user.faculty).prefetch_related('notes', 'recordings', 'assignments')
	elif user.user_type == 'student' and user.enrolled_batch:
		batches = [user.enrolled_batch]
		batches[0].notes = Note.objects.filter(batch=batches[0])
		batches[0].recordings = Recording.objects.filter(batch=batches[0])
		batches[0].assignments = Assignment.objects.filter(batch=batches[0])

	name = user.faculty.name if getattr(user, 'faculty', None) else user.username
	initials = ''
	if name:
		parts = [part for part in name.split() if part]
		if len(parts) >= 2:
			initials = f"{parts[0][0]}{parts[-1][0]}".upper()
		else:
			initials = name[:2].upper()

	return render(request, "core/dashboard.html", {
		"batches": batches,
		"profile_name": name,
		"profile_role": user.faculty.title if getattr(user, 'faculty', None) else user.current_role,
		"profile_email": user.email,
		"profile_mobile": user.mobile_number,
		"profile_batch": user.enrolled_batch,
		"profile_bio": user.faculty.bio if getattr(user, 'faculty', None) else '',
		"profile_skills": user.faculty.skill_list() if getattr(user, 'faculty', None) else [],
		"profile_initials": initials,
		"profile_user_type": user.user_type,
	})

@login_required(login_url="/login/")
def profile_update(request):
	user = request.user
	if request.method == 'POST':
		user.current_role = request.POST.get('current_role', '')
		user.mobile_number = request.POST.get('mobile_number', '')
		user.save()
		messages.success(request, 'Profile updated successfully.')
		return redirect('dashboard')

	name = user.faculty.name if getattr(user, 'faculty', None) else user.username
	initials = ''
	if name:
		parts = [part for part in name.split() if part]
		if len(parts) >= 2:
			initials = f"{parts[0][0]}{parts[-1][0]}".upper()
		else:
			initials = name[:2].upper()

	return render(request, "core/profile_update.html", {
		"profile_name": name,
		"profile_role": user.faculty.title if getattr(user, 'faculty', None) else user.current_role,
		"profile_email": user.email,
		"profile_mobile": user.mobile_number,
		"profile_batch": user.enrolled_batch,
		"profile_bio": user.faculty.bio if getattr(user, 'faculty', None) else '',
		"profile_skills": user.faculty.skill_list() if getattr(user, 'faculty', None) else [],
		"profile_initials": initials,
	})

def login_view(request):
	if request.method == "POST":
		username = request.POST["username"]
		password = request.POST["password"]
		user = authenticate(request, username=username, password=password)
		if user is not None:
			login(request, user)
			return redirect("/home/")
		else:
			return render(request, "core/login.html", {"error": "Invalid credentials"})
	return render(request, "core/login.html")

def logout_view(request):
	logout(request)
	return redirect("landing")


# Admissions form handling
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def admissions_apply(request):
	if request.method == "POST":
		full_name = request.POST.get("full_name")
		email = request.POST.get("email")
		motivation = request.POST.get("motivation")
		Admission.objects.create(full_name=full_name, email=email, motivation=motivation)
		messages.success(request, "Application submitted successfully!")
		return redirect("landing")
	return redirect("landing")


