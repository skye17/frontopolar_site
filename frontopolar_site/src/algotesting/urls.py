from django.conf.urls import url
from django.conf import settings
from django.views.static import serve

from . import views

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'test/$', views.test, name='testing'),
    url(r'about/$', views.AboutView.as_view(), name='about'),
    url(r'team/$', views.TeamView.as_view(), name='team'),
    url(r'add/$', views.AddView.as_view(), name = 'add'),
    url(r'archive/$', views.ArchiveView.as_view(), name = 'archive'),
    url(r'quick_start/$', views.quick_start, name='quick_start'),
    url(r'^datasetinfo/(?P<slug>(\w+.\w+))/$', views.DatasetInfoView.as_view(), name = 'dataset_info'),
    url(r'datasets/$', views.DatasetListView.as_view(), name = 'datasets'),
    url(r'algorithms/$', views.AlgoListView.as_view(), name = 'algorithms'),
    url(r'add_dataset/$', views.UploadDatasetFormView.as_view(), name = 'add_dataset'),
    url(r'add_algorithm/$', views.UploadAlgorithmFormView.as_view(), name = 'add_algorithm'),
    url(r'test_results/(?P<pk>\d+)/$', views.TestResult.as_view(), name='test_results'),
]

if settings.DEBUG:
    urlpatterns += [url(r'uploads/(?P<path>.*)',serve, {'document_root': settings.MEDIA_ROOT})]
