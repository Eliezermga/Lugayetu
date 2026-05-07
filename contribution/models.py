from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from core.models import Language
import os

class ContributionAudio(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="audio_contributions", verbose_name=_("Contributeur"))
    language = models.ForeignKey(Language, on_delete=models.CASCADE, related_name="audio_contributions", verbose_name=_("Langue"))
    phrase_native = models.TextField(verbose_name=_("Phrase originale"))
    phrase_translation = models.TextField(verbose_name=_("Traduction (Français)"))
    audio_file = models.FileField(upload_to='audio/temp/', verbose_name=_("Fichier audio"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Date de création"))

    class Meta:
        verbose_name = _("Contribution Audio")
        verbose_name_plural = _("Contributions Audio")

    def __str__(self):
        return f"Audio {self.language.name} - {self.user.email}"

    def save(self, *args, **kwargs):
        if not self.pk:
            # Generate the dynamic path: audio/nom_de_la_langue/nom_du_fichier.wav
            filename = f"{self.user.id}_{self.language.code}_{os.path.basename(self.audio_file.name)}"
            self.audio_file.name = os.path.join('audio', self.language.name, filename)
        super().save(*args, **kwargs)

class ContributionText(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="text_contributions", verbose_name=_("Contributeur"))
    language = models.ForeignKey(Language, on_delete=models.CASCADE, related_name="text_contributions", verbose_name=_("Langue"))
    phrase_native = models.TextField(verbose_name=_("Phrase originale"))
    phrase_french = models.TextField(verbose_name=_("Phrase en Français"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Date de création"))

    class Meta:
        verbose_name = _("Contribution Texte")
        verbose_name_plural = _("Contributions Texte")

    def __str__(self):
        return f"Texte {self.language.name} - {self.user.email}"
