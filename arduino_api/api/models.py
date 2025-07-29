from django.db import models

class LightEvent(models.Model):
    STATO_CHOICES = [
        ('accesa', 'Luce Accesa'),
        ('spenta', 'Luce Spenta'),
    ]
    
    stato = models.CharField(max_length=10, choices=STATO_CHOICES)
    timestamp = models.DateTimeField(auto_now_add=True)
    valore_sensore = models.IntegerField(null=True, blank=True)  # Valore opzionale del fotoresistore
    
    class Meta:
        ordering = ['-timestamp']
        verbose_name = 'Evento Luce'
        verbose_name_plural = 'Eventi Luce'
    
    def __str__(self):
        return f"{self.get_stato_display()} - {self.timestamp.strftime('%d/%m/%Y %H:%M:%S')}"

class LightStatus(models.Model):
    """Modello opzionale per tenere traccia dello stato corrente"""
    is_on = models.BooleanField(default=False)
    ultimo_cambio = models.DateTimeField(auto_now=True)
    soglia = models.IntegerField(default=500)  # Soglia fotoresistore
    
    class Meta:
        verbose_name = 'Stato Corrente Luce'
        verbose_name_plural = 'Stato Corrente Luce'
    
    def save(self, *args, **kwargs):
        # Assicura che ci sia solo un record
        self.__class__.objects.exclude(id=self.id).delete()
        super().save(*args, **kwargs)