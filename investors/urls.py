from django.urls import path
from .views import become_investor
from .views import check_investor_profile
from .views import investment_dashboard
from .views import MyInvestmentView, InvestmentDetailView, InvestorPortfolioView
from .views import investissement, initiate_investment, annuler_investissement
from .product_view import (
    initiate_purchass, 
    set_achat_quantity, 
    MyAchats,
    AchatDetailView,
    annuler_achat
)

app_name = "investor"
urlpatterns = [
    path('become/', become_investor, name='become-investor'),
    path('profile_check/', check_investor_profile, name='check-investor-profile'),
    path('investmentdetail/<uuid:uid>/',InvestmentDetailView.as_view(),name="investment-details"),
    path('investment/initiate/<uuid:uid>/', initiate_investment, name='investment-initiate'),
    path('achat/initiate/<uuid:uid>/', initiate_purchass, name='achat-initiate'),
    path('investment/create/<uuid:uid>/', investissement, name='investissement'),
    path('achat/<uuid:uid>/', set_achat_quantity, name='achat'),
    path('achat/detail/<uuid:uid>/', AchatDetailView.as_view(), name='achat-details'),
    path('achat/annuler/<uuid:uid>/', annuler_achat, name='annuler-achat'),
    path('annuler-investissement/<uuid:uid>/', annuler_investissement, name='annuler_investissement'),
    path('my_investments/',MyInvestmentView.as_view(),name="my-investments"),
    path('mes-achats/',MyAchats.as_view(),name="mes-achats"),
    path('vallet/',InvestorPortfolioView.as_view(),name="my-vallet"),
    path('dashboard/', investment_dashboard, name='investment-dashboard'),
]