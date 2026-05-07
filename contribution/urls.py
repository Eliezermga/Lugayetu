from django.urls import path
from . import views

app_name = 'contribution'

urlpatterns = [
    path('dashboard/', views.ContributionDashboardView.as_view(), name='dashboard'),
    path('audio/', views.AudioContributionView.as_view(), name='audio_recording'),
    path('text/', views.TextContributionView.as_view(), name='text_registration'),
    path('api/save-audio/', views.SaveAudioContributionView.as_view(), name='save_audio'),
    path('api/save-text/', views.SaveTextContributionView.as_view(), name='save_text'),
    path('api/get-next-phrase/', views.GetNextPhraseView.as_view(), name='get_next_phrase'),
]
