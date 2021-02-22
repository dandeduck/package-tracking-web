from packages.models import City, Package, Street

def string_data_lists_context():
    return {
        'cities': City.objects.all(),
        'streets': Street.objects.all(),
        'names': Package.objects.exclude(full_name='').values_list('full_name', flat=True)
    }