from django.urls import path

from user_panel_module import views

urlpatterns = [
 path('', views.UserPanelDashboardView.as_view(), name='user_panel_dashboard_page'),
 path('edit-profile/', views.EditProfileView.as_view(), name='edit_profile_page'),
 path('change-password/', views.ChangePasswordView.as_view(), name='change_password_page'),
 path('user-basket/', views.user_basket, name='user_basket_page'),
 path('order-list/', views.OrderListView.as_view(), name='order_list_page'),
 path('order-detail/<order_id>', views.order_detail, name='order_detail_page'),
 path('remove-order-detail/', views.remove_order_detail, name='remove-order-detail_page'),
 path('change-order-quantity', views.change_order_quantity, name='change-order-quantity_page'),
]
