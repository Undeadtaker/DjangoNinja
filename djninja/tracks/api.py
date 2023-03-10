from typing import List, Optional
from ninja import NinjaAPI
from tracks.models import Track
from tracks.schema import TrackSchema, NotFoundSchema

api = NinjaAPI()


# Get a list of all tracks. Filtering can be done by passing a filter parameter
# Filter by word
@api.get('/tracks', response=List[TrackSchema])
def tracks(request, title: Optional[str] = None):
    if title:
        return Track.objects.filter(title__icontains=title)
    return Track.objects.all()


# Post a new track
@api.post('/tracks', response={201: TrackSchema})
def create_track(request, track: TrackSchema):
    track = Track.objects.create(**track.dict())
    return track


# Update a track
@api.put('/tracks/{track_id}', response={200: TrackSchema, 404: NotFoundSchema})
def update_track(request, track_id: int, data: TrackSchema):
    try:
        track = Track.objects.get(pk=track_id)
        for attribute, value in data.dict().items():
            setattr(track, attribute, value)
        track.save()
        return 200, track
    except Track.DoesNotExist as e:
        return 404, {'message': 'Track with this ID does not exist'}


# Delete a track
@api.delete("/tracks/{track_id}", response={200: str, 404: NotFoundSchema})
def delete_track(request, track_id: int):
    try:
        track = Track.objects.get(pk=track_id)
        track.delete()
        return 200, f'Track with Id {track_id} has been deleted'
    except Track.DoesNotExist as e:
        return 404, {"message": "Could not find track"}

# Get track by ID
@api.get('/track/{track_id}', response={200: TrackSchema, 404: NotFoundSchema})
def track(request, track_id: int):
    try:
        track = Track.objects.get(pk=track_id)
        return 200, track
    except Track.DoesNotExist as e:
        return 404, {'message': 'Track with this ID does not exist'}















