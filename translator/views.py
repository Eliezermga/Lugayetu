from django.shortcuts import render
from django.views.generic import TemplateView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import TranslateSerializer
from .models import TranslationModel
from django.utils.translation import gettext_lazy as _

class TranslatorView(TemplateView):
    template_name = 'pages/translator.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = _("Traducteur Ruund - Français")
        return context

class TranslateAPIView(APIView):
    """
    Endpoint API pour traiter les demandes de traduction.
    POST /translator/api/translate/
    """
    def post(self, request):
        serializer = TranslateSerializer(data=request.data)
        if serializer.is_valid():
            text = serializer.validated_data['text']
            src_lang = serializer.validated_data['src_lang']
            tgt_lang = serializer.validated_data['tgt_lang']
            
            # Déterminer quel modèle utiliser
            model_type = "ruu_fr" if src_lang == "ruu_CM" else "fr_ruu"
            
            # Appel du Singleton/Manager
            model = TranslationModel(model_type=model_type)
            translation = model.translate(text, src_lang, tgt_lang)
            
            return Response({
                'original': text,
                'translation': translation,
                'src_lang': src_lang,
                'tgt_lang': tgt_lang
            }, status=status.HTTP_200_OK)
            
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
