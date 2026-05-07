
# GraphQL Schema
# backend/rama_gallery/api/schema.py
import graphene
from graphene_django import DjangoObjectType
from django.db.models import Count, Sum, Q
from datetime import datetime, timedelta
from rama_gallery.apps.users.models import USERS, USER_ACTIVITY_LOGS
from rama_gallery.apps.content.models import CONTENT_ITEMS, LIKES, COMMENTS, VIEWS_TRACKING
from rama_gallery.apps.websocket.models import CHAT_MESSAGES

class UserType(DjangoObjectType):
    class Meta:
        model = USERS
        fields = ('ID', 'USERNAME', 'EMAIL', 'AVATAR_URL', 'CREATED_AT', 'LAST_LOGIN')

class ActivityLogType(DjangoObjectType):
    class Meta:
        model = USER_ACTIVITY_LOGS
        fields = ('ID', 'USER_ID', 'ACTION_TYPE', 'ACTION_DETAILS', 'CREATED_AT')

class ContentType(DjangoObjectType):
    class Meta:
        model = CONTENT_ITEMS
        fields = ('ID', 'TITLE', 'DESCRIPTION', 'VIEWS_COUNT', 'LIKES_COUNT', 'COMMENTS_COUNT', 'CREATED_AT')

class DashboardStats(graphene.ObjectType):
    total_users = graphene.Int()
    new_users_today = graphene.Int()
    total_views = graphene.Int()
    total_likes = graphene.Int()
    total_comments = graphene.Int()
    total_chat_messages = graphene.Int()
    active_users_24h = graphene.Int()
    
class HourlyStat(graphene.ObjectType):
    hour = graphene.Int()
    count = graphene.Int()

class ContentPerformance(graphene.ObjectType):
    id = graphene.Int()
    title = graphene.String()
    views_count = graphene.Int()
    likes_count = graphene.Int()
    comments_count = graphene.Int()

class TopUser(graphene.ObjectType):
    username = graphene.String()
    content_count = graphene.Int()
    likes_received = graphene.Int()
    comments_made = graphene.Int()

class Query(graphene.ObjectType):
    dashboard_stats = graphene.Field(DashboardStats)
    recent_activities = graphene.List(ActivityLogType, limit=graphene.Int(default_value=20))
    content_performance = graphene.List(ContentPerformance, limit=graphene.Int(default_value=10))
    hourly_stats = graphene.List(HourlyStat, date=graphene.Date())
    top_users = graphene.List(TopUser, limit=graphene.Int(default_value=10))
    
    def resolve_dashboard_stats(self, info):
        from rama_gallery.apps.analytics.models import analytics_manager
        stats = analytics_manager.get_dashboard_stats()
        return DashboardStats(
            total_users=stats['total_users'],
            new_users_today=stats['new_users_today'],
            total_views=stats['total_views'],
            total_likes=stats['total_likes'],
            total_comments=stats['total_comments'],
            total_chat_messages=stats['total_chat_messages'],
            active_users_24h=stats['active_users_24h']
        )
    
    def resolve_recent_activities(self, info, limit=20):
        from rama_gallery.apps.analytics.models import analytics_manager
        return analytics_manager.get_recent_activities(limit)
    
    def resolve_content_performance(self, info, limit=10):
        from rama_gallery.apps.analytics.models import analytics_manager
        return analytics_manager.get_content_performance()[:limit]
    
    def resolve_hourly_stats(self, info, date=None):
        from rama_gallery.apps.analytics.models import analytics_manager
        if not date:
            date = datetime.now().date()
        return analytics_manager.get_hourly_stats(date)
    
    def resolve_top_users(self, info, limit=10):
        from rama_gallery.apps.analytics.models import analytics_manager
        return analytics_manager.get_top_users()[:limit]

schema = graphene.Schema(query=Query)