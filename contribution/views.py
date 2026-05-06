import json
from django.shortcuts import render, redirect
from django.views.generic import TemplateView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.utils.translation import gettext as _
from .models import ContributionAudio, ContributionText
from .utils import get_random_phrase_for_language
from core.models import Language

class ContributionDashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'contribution/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['languages'] = Language.objects.filter(is_active=True)
        return context

class AudioContributionView(LoginRequiredMixin, TemplateView):
    template_name = 'contribution/audio_recording.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Use user's mother tongue by default if available
        user_lang = self.request.user.mother_tongue
        if not user_lang:
            # Fallback to the first active language
            user_lang = Language.objects.filter(is_active=True).first()
        
        context['selected_language'] = user_lang
        context['phrase'] = get_random_phrase_for_language(user_lang.name) if user_lang else None
        return context

class TextContributionView(LoginRequiredMixin, TemplateView):
    template_name = 'contribution/text_registration.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['languages'] = Language.objects.filter(is_active=True)
        return context

class SaveAudioContributionView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        audio_data = request.FILES.get('audio_data')
        language_id = request.POST.get('language_id')
        phrase_native = request.POST.get('phrase_native')
        phrase_translation = request.POST.get('phrase_translation')

        if not all([audio_data, language_id, phrase_native, phrase_translation]):
            return JsonResponse({'status': 'error', 'message': _('Données incomplètes')}, status=400)

        try:
            language = Language.objects.get(id=language_id)
            contribution = ContributionAudio.objects.create(
                user=request.user,
                language=language,
                phrase_native=phrase_native,
                phrase_translation=phrase_translation,
                audio_file=audio_data
            )
            return JsonResponse({'status': 'success', 'message': _('Contribution enregistrée avec succès')})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

class SaveTextContributionView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        language_id = request.POST.get('language_id')
        phrase_native = request.POST.get('phrase_native')
        phrase_french = request.POST.get('phrase_french')

        if not all([language_id, phrase_native, phrase_french]):
            return JsonResponse({'status': 'error', 'message': _('Données incomplètes')}, status=400)

        try:
            language = Language.objects.get(id=language_id)
            ContributionText.objects.create(
                user=request.user,
                language=language,
                phrase_native=phrase_native,
                phrase_french=phrase_french
            )
            return JsonResponse({'status': 'success', 'message': _('Paire de phrases enregistrée')})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

class GetNextPhraseView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        language_id = request.GET.get('language_id')
        try:
            language = Language.objects.get(id=language_id)
            phrase = get_random_phrase_for_language(language.name)
            if phrase:
                return JsonResponse({'status': 'success', 'phrase': phrase})
            else:
                return JsonResponse({'status': 'empty', 'message': _('Aucune phrase disponible pour cette langue')})
        except Language.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': _('Langue non trouvée')}, status=404)
