from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import ContributionAudio, ContributionText


@admin.register(ContributionAudio)
class ContributionAudioAdmin(admin.ModelAdmin):
    list_display = ('user', 'language', 'phrase_native', 'created_at')
    list_filter = ('language', 'created_at')
    search_fields = ('user__email', 'user__first_name', 'phrase_native')
    readonly_fields = ('audio_file', 'created_at')
    ordering = ('-created_at',)


@admin.register(ContributionText)
class ContributionTextAdmin(admin.ModelAdmin):
    list_display = ('user', 'language', 'phrase_native', 'phrase_french', 'created_at')
    list_filter = ('language', 'created_at')
    search_fields = ('user__email', 'user__first_name', 'phrase_native', 'phrase_french')
    ordering = ('-created_at',)
