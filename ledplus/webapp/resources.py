from import_export import resources
from .models import Sale

class RateResource(resources.ModelResource):
    class Meta:
        model = Sale