from django.urls import path
from .views import RegisterView, LoginView, UserDetailView, UsersView, OrganisationListView, OrganisationDetailView, OrganisationCreateView, AddUserToOrganisationView

urlpatterns = [
    path('auth/register', RegisterView.as_view(), name='register'),
    path('auth/login', LoginView.as_view(), name='login'),
    path('api/users/', UsersView.as_view(), name='user-list'),  # For listing users
    path('api/users/<str:user_id>/', UserDetailView.as_view(), name='user-detail'),
    path('api/organisations', OrganisationListView.as_view(), name='organisation-list'),
    path('api/organisations/<uuid:org_id>', OrganisationDetailView.as_view(), name='organisation-detail'),
    path('api/organisations/create', OrganisationCreateView.as_view(), name='organisation-create'),
    path('api/organisations/<uuid:org_id>/users', AddUserToOrganisationView.as_view(), name='add-user-to-organisation'),
]