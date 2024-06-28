from django.contrib import admin
from .models import Label, Task
from django.utils.translation import gettext_lazy as _

class LabelAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner', 'created_at')
    search_fields = ('name',)
    list_filter = ('created_at',)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if not request.user.is_superuser:
            qs = qs.filter(owner=request.user)
        return qs

    # Restrict change permissions to the label's owner
    def has_change_permission(self, request, obj=None):
        if obj is not None and not request.user.is_superuser:
            return obj.owner == request.user
        return super().has_change_permission(request, obj=obj)

    # Restrict delete permissions to the label's owner
    def has_delete_permission(self, request, obj=None):
        if obj is not None and not request.user.is_superuser:
            return obj.owner == request.user
        return super().has_delete_permission(request, obj=obj)
    
class LabelNameFilter(admin.SimpleListFilter):
    title = _('Label')
    parameter_name = 'label'

    def lookups(self, request, model_admin):
        labels = Label.objects.all()
        return [(label.id, label.name) for label in labels]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(labels__id=self.value())
        return queryset

class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'completed', 'owner', 'get_labels')
    search_fields = ('title', 'description')
    list_filter = ('completed', 'created_at', 'updated_at',  LabelNameFilter)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        
        if request.user.is_superuser:
            return qs
        return qs.filter(owner=request.user)
    
    def get_labels(self, obj):
        return ", ".join([label.name for label in obj.labels.all()])
    get_labels.short_description = 'Label'

admin.site.register(Label, LabelAdmin)
admin.site.register(Task, TaskAdmin)
