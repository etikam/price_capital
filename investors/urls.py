from django.urls import path
from .views import become_investor
from .views import check_investor_profile
from .views import investment_dashboard
from .views import MyInvestmentView, InvestmentDetailView,InvestorPortfolioView
from .views import investissement, initiate_investment, annuler_investissement

app_name = "investor"
urlpatterns = [
    path('become/', become_investor, name='become-investor'),
    path('profile_check/', check_investor_profile, name='check-investor-profile'),
    path('investment/<uuid:uid>/',InvestmentDetailView.as_view(),name="investment-details"),
    path('investment/initiate/<uuid:uid>/', initiate_investment, name='investment-initiate'),
    path('investment/<uuid:uid>/', investissement, name='investissement'),
    path('annuler-investissement/<uuid:uid>/', annuler_investissement, name='annuler_investissement'),
    path('my_investments/',MyInvestmentView.as_view(),name="my-investments"),
    path('vallet/',InvestorPortfolioView.as_view(),name="my-vallet"),
    path('dashboard/', investment_dashboard, name='investment-dashboard'),
]