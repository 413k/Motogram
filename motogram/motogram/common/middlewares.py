from motogram.main.models import VehiclePhoto


def count_user_clicks_middleware(get_response):
    def middleware(request):
        clicks_count = request.session.get('clicks_count', 0)
        clicks_count += 1
        request.session['clicks_count'] = clicks_count
        request.clicks_count = clicks_count
        return get_response(request)

    return middleware


def last_viewed_vehicle_photos_middleware(get_response):
    def middleware(request):
        vehicle_photo_ids = request.session.get('last_viewed_vehicle_photo_ids', [])
        vehicles = VehiclePhoto.objects.filter(id__in=vehicle_photo_ids)
        request.last_viewed_vehicle_photos = vehicles
        return get_response(request)

    return middleware
