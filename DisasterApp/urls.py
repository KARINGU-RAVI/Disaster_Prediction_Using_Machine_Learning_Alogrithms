from django.urls import path

from . import views

urlpatterns = [path("index.html", views.index, name="index"),
	       path('UserLogin.html', views.UserLogin, name="UserLogin"), 
	       path('UserLoginAction', views.UserLoginAction, name="UserLoginAction"),
	       path('Register.html', views.Register, name="Register"), 
	       path('RegisterAction', views.RegisterAction, name="RegisterAction"),
	       path('LoadDataset', views.LoadDataset, name="LoadDataset"),
	       path('LoadDatasetAction', views.LoadDatasetAction, name="LoadDatasetAction"),
	       path('TrainML', views.TrainML, name="TrainML"),
	       path('Guidelines', views.Guidelines, name="Guidelines"),	   
	       path('Predict', views.Predict, name="Predict"),
	       path('PredictAction', views.PredictAction, name="PredictAction"),
	       path('Communication', views.Communication, name="Communication"),	  
	       path('CommunicationAction', views.CommunicationAction, name="CommunicationAction"),
	       path('ViewCommunication', views.ViewCommunication, name="ViewCommunication"),
]