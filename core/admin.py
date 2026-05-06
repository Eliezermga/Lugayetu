from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from .models import User, Language, HomePageContent, AboutPageContent, LegalPage

@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'is_active')
    search_fields = ('name', 'code')
    list_filter = ('is_active',)

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('email', 'first_name', 'last_name', 'role', 'province', 'mother_tongue', 'is_approved', 'is_staff')
    list_filter = ('role', 'is_approved', 'province', 'mother_tongue', 'is_staff')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)
    
    actions = ['approve_users']

    fieldsets = UserAdmin.fieldsets + (
        (_('Profil Lugayetu'), {'fields': ('age', 'sexe', 'mother_tongue', 'province', 'city_village', 'role', 'is_approved')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (_('Profil Lugayetu'), {'fields': ('email', 'first_name', 'last_name', 'age', 'sexe', 'mother_tongue', 'province', 'city_village', 'role', 'is_approved')}),
    )

    def approve_users(self, request, queryset):
        queryset.update(is_approved=True)
        self.message_user(request, _("Les utilisateurs sélectionnés ont été approuvés."))
    approve_users.short_description = _("Approuver les utilisateurs sélectionnés")

@admin.register(LegalPage)
class LegalPageAdmin(admin.ModelAdmin):
    list_display = ('slug', 'title_fr', 'last_updated')
    fieldsets = (
        (_('Structure'), {
            'fields': ('slug', 'title_fr', 'title_en')
        }),
        (_('Contenu'), {
            'fields': ('content_fr', 'content_en'),
            'description': _("<b>Guide de style HTML :</b><br>"
                             "Utilisez <code>&lt;h3&gt;</code> pour les titres de section.<br>"
                             "Utilisez <code>&lt;p&gt;</code> pour les paragraphes.<br>"
                             "Utilisez <code>&lt;ul&gt;</code> et <code>&lt;li&gt;</code> pour les listes à puces.<br>"
                             "Utilisez <code>&lt;strong&gt;</code> pour mettre en gras.")
        }),
    )

@admin.register(HomePageContent)
class HomePageContentAdmin(admin.ModelAdmin):
    fieldsets = (
        (_('Hero Section'), {
            'fields': ('hero_title_fr', 'hero_title_en', 'hero_description_fr', 'hero_description_en')
        }),
        (_('Stats Section'), {
            'fields': ('stats_title_fr', 'stats_title_en', 'stats_description_fr', 'stats_description_en')
        }),
        (_('Mission Section'), {
            'fields': ('mission_title_fr', 'mission_title_en')
        }),
        (_('CTA Section'), {
            'fields': ('cta_title_fr', 'cta_title_en', 'cta_description_fr', 'cta_description_en')
        }),
    )

    def has_add_permission(self, request):
        if self.model.objects.count() > 0:
            return False
        return super().has_add_permission(request)

@admin.register(AboutPageContent)
class AboutPageContentAdmin(admin.ModelAdmin):
    fieldsets = (
        (_('Header & Hero'), {
            'fields': ('title_fr', 'title_en', 'description_fr', 'description_en')
        }),
        (_('Quote'), {
            'fields': ('quote_fr', 'quote_en')
        }),
        (_('Mission & Vision'), {
            'fields': ('mission_title_fr', 'mission_title_en', 'mission_text_fr', 'mission_text_en',
                       'vision_title_fr', 'vision_title_en', 'vision_text_fr', 'vision_text_en')
        }),
        (_('Why Lugayetu'), {
            'fields': ('why_title_fr', 'why_title_en', 'why_text_fr', 'why_text_en')
        }),
        (_('History & Timeline'), {
            'fields': ('history_title_fr', 'history_title_en', 'history_json')
        }),
        (_('Team & Contact'), {
            'fields': ('team_title_fr', 'team_title_en', 'team_text_fr', 'team_text_en',
                       'contact_title_fr', 'contact_title_en', 'contact_email')
        }),
        (_('Footer Message'), {
            'fields': ('footer_message_fr', 'footer_message_en')
        }),
    )

    def has_add_permission(self, request):
        if self.model.objects.count() > 0:
            return False
        return super().has_add_permission(request)
