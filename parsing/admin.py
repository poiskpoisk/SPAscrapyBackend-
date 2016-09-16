from django.contrib import admin
from .models import StatMsg, QueneURLs, ParsingData, ScheduleQuene


class ParsingDataAdmin(admin.ModelAdmin):
    list_display    = ('id','parsingURL', 'title', 'h1', 'image_url')
    list_filter     = ['parsingURL']

admin.site.register( StatMsg )
admin.site.register(QueneURLs)
admin.site.register( ScheduleQuene )
admin.site.register( ParsingData, ParsingDataAdmin )


