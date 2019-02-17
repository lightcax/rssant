# from rest_framework import serializers
# from rest_framework.response import Response
# from rest_framework.views import APIView
from django_rest_validr import RestRouter, T

from .models import RssFeed

FeedView = RestRouter()

RssFeedSchema = T.dict(
    id=T.int,
    user_id=T.int,
    url=T.url,
    title=T.str.optional,
    dt_created=T.datetime.optional,
    dt_updated=T.datetime.optional,
)


@FeedView.get('feed/')
def feed_list(request) -> T.list(RssFeedSchema):
    """Feed list"""
    feeds = RssFeed.objects.filter(user=request.user).all()
    return feeds


@FeedView.get('feed/<int:pk>')
@FeedView.get('feed/<int:pk>/detail')
def feed_get(request, pk: T.int) -> RssFeedSchema:
    """Feed detail"""
    feed = RssFeed.objects.get(pk=pk)
    return feed


@FeedView.post('feed/')
def feed_create(request, url: T.url) -> RssFeedSchema:
    feed = RssFeed.objects.create(user=request.user, url=url)
    feed.save()
    return feed


@FeedView.delete('feed/<int:pk>')
def feed_delete(request, pk: T.int):
    feed = RssFeed.objects.get(pk=pk)
    feed.delete()
