from django.urls import path
from .views import become_investor
from .views import check_investor_profile
from .views import investment_dashboard
from .views import investissement, initiate_investment

app_name = "investor"
urlpatterns = [
    path('become/', become_investor, name='become-investor'),
    path('profile_check/', check_investor_profile, name='check-investor-profile'),
    path('dashboard/', investment_dashboard, name='investment-dashboard'),
    path('investment/initiate/<uuid:uid>/', initiate_investment, name='investment-initiate'),
    # path('investment/<uuid:uid>/', investissement, name='investissement'),
]