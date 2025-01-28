from django.urls import path

from .product_view import AchatDetailView, MyAchats, annuler_achat, initiate_purchass, set_achat_quantity
from .views import (
    InvestmentDetailView,
    InvestorPortfolioView,
    MyInvestmentView,
    annuler_investissement,
    become_investor,
    check_investor_profile,
    initiate_investment,
    investissement,
    investment_dashboard,
)

app_name = "investor"
urlpatterns = [
    path("become/", become_investor, name="become-investor"),
    path("profile_check/", check_investor_profile, name="check-investor-profile"),
    path("investmentdetail/<uuid:uid>/", InvestmentDetailView.as_view(), name="investment-details"),
    path("investment/initiate/<uuid:uid>/", initiate_investment, name="investment-initiate"),
    path("achat/initiate/<uuid:uid>/", initiate_purchass, name="achat-initiate"),
    path("investment/create/<uuid:uid>/", investissement, name="investissement"),
    path("achat/<uuid:uid>/", set_achat_quantity, name="achat"),
    path("achat/detail/<uuid:uid>/", AchatDetailView.as_view(), name="achat-details"),
    path("achat/annuler/<uuid:uid>/", annuler_achat, name="annuler-achat"),
    path("annuler-investissement/<uuid:uid>/", annuler_investissement, name="annuler_investissement"),
    path("my_investments/", MyInvestmentView.as_view(), name="my-investments"),
    path("mes-achats/", MyAchats.as_view(), name="mes-achats"),
    path("vallet/", InvestorPortfolioView.as_view(), name="my-vallet"),
    path("dashboard/", investment_dashboard, name="investment-dashboard"),
]
