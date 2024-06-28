from django.db import models

class PhoneName(models.Model):
    phone_name = models.CharField(max_length=100,null=True, blank=True)
    
    
    def __str__(self):
        return self.phone_name
    
    
    
class Product(models.Model):
    
    phone_name = models.ForeignKey(PhoneName, on_delete= models.CASCADE) 
    technology = models.TextField(blank=True)
    announced = models.CharField(max_length=100, blank=True)
    status = models.CharField(max_length=100, blank=True)
    dimensions = models.CharField(max_length=100, blank=True)
    weight = models.CharField(max_length=100, blank=True)
    build = models.TextField(blank=True)
    sim = models.CharField(max_length=100, blank=True)
    display_type = models.CharField(max_length=100, blank=True)
    display_size = models.CharField(max_length=100, blank=True)
    resolution = models.CharField(max_length=100, blank=True)
    protection = models.CharField(max_length=100, blank=True)
    os = models.CharField(max_length=100, blank=True)
    chipset = models.CharField(max_length=100, blank=True)
    cpu = models.CharField(max_length=100, blank=True)
    gpu = models.CharField(max_length=100, blank=True)
    card_slot = models.CharField(max_length=100, blank=True)
    internal = models.CharField(max_length=100, blank=True)
    main_camera = models.TextField(blank=True)
    main_camera_features = models.TextField(blank=True)
    main_camera_video = models.TextField(blank=True)
    selfie_camera = models.TextField(blank=True)
    selfie_camera_features = models.TextField(blank=True)
    selfie_camera_video = models.TextField(blank=True)
    loudspeaker = models.CharField(max_length=100, blank=True)
    headphone_jack = models.CharField(max_length=100, blank=True)
    wlan = models.CharField(max_length=100, blank=True)
    bluetooth = models.CharField(max_length=100, blank=True)
    positioning = models.CharField(max_length=100, blank=True)
    nfc = models.CharField(max_length=100, blank=True)
    radio = models.CharField(max_length=100, blank=True)
    usb = models.CharField(max_length=100, blank=True)
    sensors = models.TextField(blank=True)
    battery_type = models.CharField(max_length=100, blank=True)
    charging = models.TextField(blank=True)
    colors = models.CharField(max_length=100, blank=True)
    model_name = models.CharField(max_length=100, blank=True)
    sar = models.CharField(max_length=100, blank=True)
    sar_eu = models.CharField(max_length=100, blank=True)
    price = models.CharField(max_length=100, blank=True)
    performance = models.TextField(blank=True)
    display = models.TextField(blank=True)
    camera = models.CharField(max_length=100, blank=True)
    loudness = models.CharField(max_length=100, blank=True)
    battery = models.CharField(max_length=100, blank=True)
    battery_new = models.CharField(max_length=100, blank=True)
    others = models.CharField(max_length=100, default=None) 
    created = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now=True)
