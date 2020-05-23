from django.contrib import admin
from voting.models import Candidate, Image, Profile, Comments
# Register your models here.
admin.site.register(Candidate)
admin.site.register(Image)
admin.site.register(Profile)
admin.site.register(Comments)