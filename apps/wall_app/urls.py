from django.conf.urls import url, include
from . import views


urlpatterns = [
    url(r'^$', views.index),
    url(r'^wall$', views.wall),
    url(r'^registration$', views.registration),
    url(r'^login$', views.login),
    url(r'^log_out$', views.log_out),
    url(r'^post_massage$', views.postMassage),
    url(r'^add_comment$', views.add_Comment),
    url(r'^delete_comment/(?P<comment_id>\d+)$', views.delete_comment),
]