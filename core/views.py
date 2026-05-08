from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.translation import gettext as _
from .models import HomePageContent, AboutPageContent, LegalPage, User, Language
from .forms import RegistrationForm, LoginForm
from contribution.models import ContributionAudio
from contribution.utils import get_total_phrase_count

def home(request):
    content, created = HomePageContent.objects.get_or_create()
    stats = {
        'audio_count': ContributionAudio.objects.count(),
        'phrase_count': get_total_phrase_count(),
        'contributor_count': User.objects.filter(role='CONTRIBUTOR', is_active=True).count(),
    }
    return render(request, 'pages/home.html', {'content': content, 'stats': stats})

def about(request):
    content, created = AboutPageContent.objects.get_or_create()
    return render(request, 'pages/about.html', {'content': content})

def legal_page(request, slug):
    page = get_object_or_404(LegalPage, slug=slug)
    # Fetch all legal pages for the sidebar
    all_pages = LegalPage.objects.all().only('slug', 'title_fr', 'title_en')
    return render(request, 'pages/legal.html', {
        'page': page,
        'all_pages': all_pages
    })

def register(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, _("Votre compte a été créé avec succès ! Il est actuellement en attente d'approbation par un administrateur."))
            return redirect('login')
        else:
            messages.error(request, _("Veuillez corriger les erreurs dans le formulaire."))
    else:
        form = RegistrationForm()
    return render(request, 'pages/auth/register.html', {'form': form})

def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if user.is_approved or user.is_staff:
                login(request, user)
                messages.success(request, _("Heureux de vous revoir !"))
                return redirect('home')
            else:
                messages.error(request, _("Votre compte n'a pas encore été approuvé par un administrateur."))
        else:
            messages.error(request, _("Email ou mot de passe incorrect."))
    else:
        form = LoginForm()
    return render(request, 'pages/auth/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('home')

@login_required
def profile(request):
    return render(request, 'pages/profile.html', {
        'title': _("Mon Profil")
    })

def error_404(request, exception):
    return render(request, '404.html', status=404)

def error_500(request):
    return render(request, '500.html', status=500)

def error_403(request, exception):
    return render(request, '403.html', status=403)

def error_400(request, exception):
    return render(request, '400.html', status=400)
