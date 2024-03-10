from django.apps import AppConfig
from keras.models import load_model

class SmagriConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'smagri'
    def ready(self):
        # Load all models during application startup
        self.jowar_model = load_model('Jowar_mn.h5')
        self.gram_model = load_model('Gram_mn.h5')
        self.grapes_model = load_model('Grapes_mn.h5')
        self.ginger_model = load_model('Ginger_mn.h5')
        self.wheat_model = load_model('Wheat_mn.h5')
        self.maize_model = load_model('Maize_mn.h5')