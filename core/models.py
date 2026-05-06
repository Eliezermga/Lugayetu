import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator, MaxValueValidator

class Language(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name=_("Nom de la langue"))
    code = models.CharField(max_length=10, unique=True, verbose_name=_("Code ISO/Interne"))
    description = models.TextField(blank=True, verbose_name=_("Description"))
    is_active = models.BooleanField(default=True, verbose_name=_("Active"))

    class Meta:
        verbose_name = _("Langue")
        verbose_name_plural = _("Langues")

    def __str__(self):
        return self.name

class User(AbstractUser):
    ROLE_CHOICES = [
        ('CONTRIBUTOR', _('Contributeur')),
        ('SUB_ADMIN', _('Sous-Admin')),
        ('ADMIN', _('Administrateur')),
    ]

    SEXE_CHOICES = [
        ('M', _('Homme')),
        ('F', _('Femme')),
    ]

    PROVINCE_CHOICES = [
        ('bas_uele', _('Bas-Uele')),
        ('equateur', _('Équateur')),
        ('haut_katanga', _('Haut-Katanga')),
        ('haut_lomami', _('Haut-Lomami')),
        ('haut_uele', _('Haut-Uele')),
        ('ituri', _('Ituri')),
        ('kasai', _('Kasaï')),
        ('kasai_central', _('Kasaï-Central')),
        ('kasai_oriental', _('Kasaï-Oriental')),
        ('kinshasa', _('Kinshasa')),
        ('kongo_central', _('Kongo-Central')),
        ('kwango', _('Kwango')),
        ('kwilu', _('Kwilu')),
        ('lomami', _('Lomami')),
        ('lualaba', _('Lualaba')),
        ('mai_ndombe', _('Mai-Ndombe')),
        ('maniema', _('Maniema')),
        ('mongala', _('Mongala')),
        ('nord_kivu', _('Nord-Kivu')),
        ('nord_ubangi', _('Nord-Ubangi')),
        ('sankuru', _('Sankuru')),
        ('sud_kivu', _('Sud-Kivu')),
        ('sud_ubangi', _('Sud-Ubangi')),
        ('tanganyika', _('Tanganyika')),
        ('tshopo', _('Tshopo')),
        ('tshuapa', _('Tshuapa')),
    ]

    email = models.EmailField(_('adresse email'), unique=True)
    first_name = models.CharField(_('prénom'), max_length=150)
    last_name = models.CharField(_('nom'), max_length=150)
    
    age = models.PositiveIntegerField(
        validators=[MinValueValidator(13), MaxValueValidator(120)],
        verbose_name=_("Âge"),
        null=True, blank=True
    )
    sexe = models.CharField(max_length=1, choices=SEXE_CHOICES, verbose_name=_("Sexe"), null=True, blank=True)
    mother_tongue = models.ForeignKey(
        Language, on_delete=models.SET_NULL, null=True, blank=True, 
        verbose_name=_("Langue maternelle"),
        related_name="native_speakers"
    )
    province = models.CharField(max_length=50, choices=PROVINCE_CHOICES, verbose_name=_("Province"), null=True, blank=True)
    city_village = models.CharField(max_length=255, verbose_name=_("Ville / Village"), null=True, blank=True)
    
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='CONTRIBUTOR', verbose_name=_("Rôle"))
    is_approved = models.BooleanField(default=False, verbose_name=_("Approuvé"))
    
    # Required for unique email login
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    class Meta:
        verbose_name = _("Utilisateur")
        verbose_name_plural = _("Utilisateurs")

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.email})"

    def save(self, *args, **kwargs):
        # Only ADMINs are allowed to access the back-office (is_staff)
        if self.role == 'ADMIN':
            self.is_staff = True
            self.is_superuser = True
        else:
            self.is_staff = False
            self.is_superuser = False
        super().save(*args, **kwargs)

class HomePageContent(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    # Hero Section
    hero_title_fr = models.CharField(max_length=255, default="Préserver les voix de notre héritage")
    hero_title_en = models.CharField(max_length=255, default="Preserving the voices of our heritage")
    hero_description_fr = models.TextField(default="Nous collectons et numérisons les richesses linguistiques de la RDC. Du Rund au Kikongo, redonnons vie à chaque mot pour les générations futures.")
    hero_description_en = models.TextField(default="We collect and digitize the linguistic wealth of the DRC. From Rund to Kikongo, let's bring every word back to life for future generations.")
    
    # Stats Section
    stats_title_fr = models.CharField(max_length=255, default="Statistiques de préservation")
    stats_title_en = models.CharField(max_length=255, default="Preservation Statistics")
    stats_description_fr = models.TextField(default="Chaque jour, nos contributeurs documentent des dialectes menacés pour assurer la pérennité de notre culture commune.")
    stats_description_en = models.TextField(default="Every day, our contributors document endangered dialects to ensure the sustainability of our common culture.")
    
    # Mission Section
    mission_title_fr = models.CharField(max_length=255, default="Notre Mission")
    mission_title_en = models.CharField(max_length=255, default="Our Mission")
    
    # CTA Section
    cta_title_fr = models.CharField(max_length=255, default="Prêt à faire partie de l'histoire ?")
    cta_title_en = models.CharField(max_length=255, default="Ready to be part of history?")
    cta_description_fr = models.TextField(default="Chaque mot que vous partagez aujourd'hui est un cadeau pour les générations de demain. Rejoignez notre communauté de gardiens du savoir.")
    cta_description_en = models.TextField(default="Every word you share today is a gift for tomorrow's generations. Join our community of knowledge keepers.")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Contenu Page d'Accueil")
        verbose_name_plural = _("Contenus Page d'Accueil")

    def __str__(self):
        return _("Contenu de la Page d'Accueil")

    def save(self, *args, **kwargs):
        # Ensure only one instance exists
        if self.__class__.objects.count():
            self.pk = self.__class__.objects.first().pk
        super().save(*args, **kwargs)

    @property
    def hero_title(self):
        from django.utils import translation
        return self.hero_title_fr if translation.get_language() == 'fr' else self.hero_title_en

    @property
    def hero_description(self):
        from django.utils import translation
        return self.hero_description_fr if translation.get_language() == 'fr' else self.hero_description_en

    @property
    def stats_title(self):
        from django.utils import translation
        return self.stats_title_fr if translation.get_language() == 'fr' else self.stats_title_en

    @property
    def stats_description(self):
        from django.utils import translation
        return self.stats_description_fr if translation.get_language() == 'fr' else self.stats_description_en

    @property
    def mission_title(self):
        from django.utils import translation
        return self.mission_title_fr if translation.get_language() == 'fr' else self.mission_title_en

    @property
    def cta_title(self):
        from django.utils import translation
        return self.cta_title_fr if translation.get_language() == 'fr' else self.cta_title_en

    @property
    def cta_description(self):
        from django.utils import translation
        return self.cta_description_fr if translation.get_language() == 'fr' else self.cta_description_en

class AboutPageContent(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    title_fr = models.CharField(max_length=255, default="À propos de Lugayetu")
    title_en = models.CharField(max_length=255, default="About Lugayetu")
    
    description_fr = models.TextField(default="Lugayetu est un projet scientifique et culturel dédié à la préservation, la documentation et la valorisation des langues en danger de la République Démocratique du Congo.")
    description_en = models.TextField(default="Lugayetu is a scientific and cultural project dedicated to the preservation, documentation, and promotion of endangered languages in the Democratic Republic of Congo.")
    
    mission_title_fr = models.CharField(max_length=255, default="Notre mission")
    mission_title_en = models.CharField(max_length=255, default="Our mission")
    mission_text_fr = models.TextField(default="Collecter et archiver la richesse linguistique congolaise avant qu'elle ne disparaisse, en permettant aux locuteurs natifs d'enregistrer leur voix et de contribuer à un corpus unique de langues menacées.")
    mission_text_en = models.TextField(default="Collect and archive the Congolese linguistic wealth before it disappears, allowing native speakers to record their voice and contribute to a unique corpus of endangered languages.")
    
    vision_title_fr = models.CharField(max_length=255, default="Notre vision")
    vision_title_en = models.CharField(max_length=255, default="Our vision")
    vision_text_fr = models.TextField(default="Créer une bibliothèque vivante des langues congolaises accessible aux chercheurs, aux éducateurs et aux générations futures.")
    vision_text_en = models.TextField(default="Create a living library of Congolese languages accessible to researchers, educators, and future generations.")
    
    why_title_fr = models.CharField(max_length=255, default="Pourquoi Lugayetu ?")
    why_title_en = models.CharField(max_length=255, default="Why Lugayetu?")
    why_text_fr = models.TextField(default="La RDC compte plus de 200 langues, dont plusieurs risquent de disparaître. Chaque langue qui s'éteint emporte avec elle une culture, une histoire et une vision unique du monde. Lugayetu veut inverser cette tendance.")
    why_text_en = models.TextField(default="The DRC has more than 200 languages, many of which are in danger of disappearing. Each language that dies takes with it a culture, a history, and a unique worldview. Lugayetu aims to reverse this trend.")
    
    team_title_fr = models.CharField(max_length=255, default="Notre équipe")
    team_title_en = models.CharField(max_length=255, default="Our team")
    team_text_fr = models.TextField(default="Le projet est porté par des linguistes, des développeurs et des passionnés de la culture congolaise, avec le soutien d'institutions académiques et culturelles.")
    team_text_en = models.TextField(default="The project is led by linguists, developers, and lovers of Congolese culture, with the support of academic and cultural institutions.")
    
    contact_title_fr = models.CharField(max_length=255, default="Contact")
    contact_title_en = models.CharField(max_length=255, default="Contact")
    contact_email = models.CharField(max_length=255, default="eliezermunung@outlook.fr")
    
    footer_message_fr = models.CharField(max_length=255, default="Merci de contribuer à la préservation du patrimoine linguistique congolais !")
    footer_message_en = models.CharField(max_length=255, default="Thank you for contributing to the preservation of the Congolese linguistic heritage!")
    
    # New fields for Stitch design alignment
    quote_fr = models.TextField(default="Perdre sa langue, c'est perdre sa boussole culturelle.")
    quote_en = models.TextField(default="To lose one's language is to lose one's cultural compass.")
    
    history_title_fr = models.CharField(max_length=255, default="Notre parcours")
    history_title_en = models.CharField(max_length=255, default="Our journey")
    
    history_json = models.JSONField(default=list, help_text="List of objects with 'year', 'title', 'text' (fr/en keys)")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Contenu Page À propos")
        verbose_name_plural = _("Contenus Page À propos")

    def __str__(self):
        return _("Contenu de la Page À propos")

    def save(self, *args, **kwargs):
        if self.__class__.objects.count():
            self.pk = self.__class__.objects.first().pk
        super().save(*args, **kwargs)

    @property
    def title(self):
        from django.utils import translation
        return self.title_fr if translation.get_language() == 'fr' else self.title_en

    @property
    def description(self):
        from django.utils import translation
        return self.description_fr if translation.get_language() == 'fr' else self.description_en

    @property
    def mission_title(self):
        from django.utils import translation
        return self.mission_title_fr if translation.get_language() == 'fr' else self.mission_title_en

    @property
    def mission_text(self):
        from django.utils import translation
        return self.mission_text_fr if translation.get_language() == 'fr' else self.mission_text_en

    @property
    def vision_title(self):
        from django.utils import translation
        return self.vision_title_fr if translation.get_language() == 'fr' else self.vision_title_en

    @property
    def vision_text(self):
        from django.utils import translation
        return self.vision_text_fr if translation.get_language() == 'fr' else self.vision_text_en

    @property
    def why_title(self):
        from django.utils import translation
        return self.why_title_fr if translation.get_language() == 'fr' else self.why_title_en

    @property
    def why_text(self):
        from django.utils import translation
        return self.why_text_fr if translation.get_language() == 'fr' else self.why_text_en

    @property
    def team_title(self):
        from django.utils import translation
        return self.team_title_fr if translation.get_language() == 'fr' else self.team_title_en

    @property
    def team_text(self):
        from django.utils import translation
        return self.team_text_fr if translation.get_language() == 'fr' else self.team_text_en

    @property
    def contact_title(self):
        from django.utils import translation
        return self.contact_title_fr if translation.get_language() == 'fr' else self.contact_title_en

    @property
    def footer_message(self):
        from django.utils import translation
        return self.footer_message_fr if translation.get_language() == 'fr' else self.footer_message_en

    @property
    def quote(self):
        from django.utils import translation
        return self.quote_fr if translation.get_language() == 'fr' else self.quote_en

    @property
    def history_title(self):
        from django.utils import translation
        return self.history_title_fr if translation.get_language() == 'fr' else self.history_title_en

    @property
    def history(self):
        from django.utils import translation
        lang = translation.get_language()
        if not self.history_json:
            return [
                {"year": "2025", "title": "Debut" if lang == 'fr' else "Beigein", "text": "De chercheurs de l'Université Nouveuax Horizons constatent la disparition progressive des langues congolaises." if lang == 'fr' else "Researchers at the Université Nouveuax Horizons observe the rapid disappearance of Congolese languages."},
                {"year": "2026", "title": "Premier Corpus" if lang == 'fr' else "First Corpus", "text": "Publication de la première version du corpus parallel Rund-Français, collectant plus de 8,000 phrases" if lang == 'fr' else "The first version of the parallel Rund-French corpus is published, collecting more than 8,000 phrases"},
                {"year": "2026", "title": "Premiere Utilisation" if lang == 'fr' else "First Model", "text": "Lugayetu fine-tune son premier model de traduction text-to-text entre le Rund et le Français. Les premiers résultats sont très encourageants." if lang == 'fr' else "Lugayetu fine-tunes its first text-to-text translation model between Rund and French. The first results are very encouraging."}
            ]
        
        processed_history = []
        for item in self.history_json:
            processed_item = {"year": item.get("year", "")}
            # Handle bilingual titles
            processed_item["title"] = item.get(f"title_{lang}", item.get("title", ""))
            # Handle bilingual texts
            processed_item["text"] = item.get(f"text_{lang}", item.get("text", ""))
            processed_history.append(processed_item)
            
        return processed_history

class LegalPage(models.Model):
    """
    Model for legal pages (Privacy Policy, Terms of Use, etc.)
    """
    PAGE_TYPES = [
        ('privacy', _('Politique de Confidentialité')),
        ('terms', _('Conditions d\'Utilisation')),
        ('legal', _('Mentions Légales')),
    ]

    slug = models.SlugField(unique=True, choices=PAGE_TYPES, help_text=_("Identifiant technique de la page"))
    
    title_fr = models.CharField(max_length=255, verbose_name=_("Titre (FR)"))
    title_en = models.CharField(max_length=255, verbose_name=_("Titre (EN)"))
    
    content_fr = models.TextField(
        verbose_name=_("Contenu (FR)"), 
        help_text=_("Utilisez des balises HTML pour la structure : <br><b>&lt;h3&gt;</b> Titre de section <br><b>&lt;p&gt;</b> Paragraphe <br><b>&lt;ul&gt;&lt;li&gt;</b> Listes <br><b>&lt;strong&gt;</b> Texte important")
    )
    content_en = models.TextField(
        verbose_name=_("Contenu (EN)"), 
        help_text=_("Use HTML tags for structure: <br><b>&lt;h3&gt;</b> Section Title <br><b>&lt;p&gt;</b> Paragraph <br><b>&lt;ul&gt;&lt;li&gt;</b> Lists <br><b>&lt;strong&gt;</b> Important text")
    )
    
    last_updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Page Légale")
        verbose_name_plural = _("Pages Légales")

    def __str__(self):
        return self.get_slug_display()

    @property
    def title(self):
        from django.utils import translation
        return self.title_fr if translation.get_language() == 'fr' else self.title_en

    @property
    def content(self):
        from django.utils import translation
        return self.content_fr if translation.get_language() == 'fr' else self.content_en

