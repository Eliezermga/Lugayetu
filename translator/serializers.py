from rest_framework import serializers

class TranslateSerializer(serializers.Serializer):
    """Séreialiseur pour valider la requête de traduction"""
    text = serializers.CharField(max_length=2000, help_text="Le texte à traduire")
    src_lang = serializers.CharField(max_length=10, default="ruu_CM")
    tgt_lang = serializers.CharField(max_length=10, default="fr_XX")
