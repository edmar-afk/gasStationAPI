from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


urlpatterns = [
    path('register/', views.CreateUserView.as_view(), name='register'),
    path('token/', TokenObtainPairView.as_view(), name='get_token'),
    path('token/refresh', TokenRefreshView.as_view(), name='refresh_token'),
    
    
    path('profile/update/', views.UpdateUserView.as_view(), name='update-profile'),
    path('user/', views.UserDetailView.as_view(), name='user_detail'),
    path('profile/<int:user_id>/', views.ProfileDetailView.as_view(), name='profile-detail'),
    
    path('gasoline/create/', views.GasolineCreateView.as_view(), name='gasoline-create'),
    path('gasoline/', views.GasolineListView.as_view(), name='gasoline-list'),
    path('active-promo/', views.ActivePromoCreateView.as_view(), name='active-promo-create'),
    path('user-promos/', views.UserPromosView.as_view(), name='user-promos'),
    
    path('delete-promo/<int:pk>/', views.ActivePromoDeleteView.as_view(), name='active-promo-delete'),
    path('search/<str:last_name>/', views.UserListByLastNameView.as_view(), name='user-list-by-last-name'),
    path('gasoline/<int:id>/delete/', views.GasolineDeleteAPIView.as_view(), name='gasoline-delete'),
    
    
    path('gasoline/<int:id>/update/', views.GasolineUpdateAPIView.as_view(), name='gasoline-update'),
    path('view-gasoline/<int:id>/', views.GasolineDetailView.as_view(), name='gasoline-filter-by-id'),
]