from django.conf.urls import url 
from athena import views

urlpatterns = [
    url(r'^$', views.ChatbotView.as_view(), name='chatbot')
]





# from django.conf.urls import url

# urlpatterns = [
#     url(r'^$', ChatbotView.as_view(), name='chatbot')
# ]