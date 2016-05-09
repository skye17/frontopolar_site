from django.shortcuts import render, redirect
from django.views.generic import TemplateView, DetailView, ListView, FormView, CreateView
from django.core.urlresolvers import reverse
from forms import QuickStartForm, UploadDataFilesForm, TestingForm, UploadAlgorithmFileForm
from models import Dataset, ExperimentResult, Algorithm
from code.sample import handle_algorithm_testing
import matplotlib.pyplot as plt
import os

class IndexView(TemplateView):
    template_name = "index.html"

class AboutView(TemplateView):
    template_name = "about.html"

class TeamView(TemplateView):
    template_name = "team.html"

class AddView(TemplateView):
    template_name = "add.html"

class ArchiveView(TemplateView):
    template_name = "archive.html"

class DatasetInfoView(DetailView):
    model = Dataset
    template_name = 'algotesting/dataset_page.html'
    slug_field = 'name'

class DatasetListView(ListView):
    template_name = 'algotesting/datasets.html'
    form_class = UploadDataFilesForm
    context_object_name = 'datasets'
    paginate_by = 20
    def get_queryset(self):
        return Dataset.objects.all()

    def get_context_data(self, **kwargs):
        context = super(DatasetListView, self).get_context_data(**kwargs)
        context['form'] = UploadDataFilesForm
        return context

class AlgoListView(ListView):
    template_name = 'algotesting/algorithms.html'
    form_class = UploadAlgorithmFileForm
    context_object_name = 'algorithms'
    paginate_by = 20
    def get_queryset(self):
        return Algorithm.objects.all()

    def get_context_data(self, **kwargs):
        context = super(AlgoListView, self).get_context_data(**kwargs)
        context['form'] = UploadAlgorithmFileForm
        return context

class UploadDatasetFormView(FormView):
    form_class = UploadDataFilesForm
    template_name = "algotesting/upload_dataset.html"
    def form_valid(self, form):
        d = form.save(commit=False)
        file = form.cleaned_data['data']
        d.filename = str(file)
        for file_line in file:
            d.columns = file_line[:-1]
            break
        d.save()
        return super(UploadDatasetFormView, self).form_valid(form)
    def get_success_url(self):
        return reverse('algotesting:datasets')

class UploadAlgorithmFormView(FormView):
    form_class = UploadAlgorithmFileForm
    template_name = "algotesting/upload_algorithm.html"
    def form_valid(self, form):
        d = form.save(commit=False)
        file = form.cleaned_data['algorithm']
        d.filename = str(file)
        d.save()
        return super(UploadAlgorithmFormView, self).form_valid(form)
    def get_success_url(self):
        return reverse('algotesting:algorithms')


def quick_start(request):
    if request.method == 'POST':
        form = QuickStartForm(request.POST)
        if form.is_valid():
            algorithm = Algorithm.objects.get(filename='user_defined.py')
            data = Dataset.objects.get(filename='daily1.csv')
            symbols = form.cleaned_data['stocks']
            capital = form.cleaned_data['base_capital']
            train_size = form.cleaned_data['train_size']
            params = {'algorithm':algorithm.filename, 'data_filenames': [data.filename], 'frequency':data.frequency,
                      'base_capital':capital,
                      'symbols':symbols.split(','), 'parser':data.date_format, 'train_size':train_size,
                      'load_file':'', 'save_file':''}
            result = handle_algorithm_testing(params)

            info = ''
            for key, value in params.items():
                if value:
                    if type(value) is list:
                        info += "{}:{}\n".format(key, ', '.join(map(str, value)))
                    else:
                        info += "{}:{}\n".format(key,value)
            experiment_info = info

            experiment_result = ExperimentResult(info = experiment_info,results_path = '')
            experiment_result.save()
            relative_path = 'testing/results/quick_start.pdf'
            graph_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
                                      'uploads/'+relative_path)

            result.savefig(graph_path)
            plt.close(result)

            experiment_result.results_path = relative_path
            experiment_result.save()

            return redirect(experiment_result)

    else:
        form = QuickStartForm()
        return render(request, 'algotesting/quick_start.html', {'form': form})

def test(request):
    if request.method == 'POST':
        form = TestingForm(request.POST)
        if form.is_valid():
            algorithm = form.cleaned_data['algorithm'][0]
            datasets = form.cleaned_data['dataset']
            load = form.cleaned_data['load_parameters']
            save = form.cleaned_data['save_parameters']
            load_params = ''
            save_params = ''
            print load,save
            if load and algorithm.train_parameters:
                load_params = algorithm.train_parameters.name
            if save:
                save_params = algorithm.train_parameters.name
            data_filenames = []
            for dataset in datasets:
                data_filenames.append(dataset.filename)
                frequency = dataset.frequency
                parser = dataset.date_format
            capital = form.cleaned_data['base_capital']
            symbols = form.cleaned_data['stocks']
            train_size = form.cleaned_data['train_size']
            params = {'algorithm':algorithm.filename,'data_filenames': data_filenames, 'frequency':frequency,
                      'base_capital':capital,
                      'symbols':symbols.split(','), 'parser':parser, 'train_size':train_size,
                      'load_file':load_params, 'save_file':save_params}
            result = handle_algorithm_testing(params)
            info = ''
            for key, value in params.items():
                if value:
                    if type(value) is list:
                        info += "{}:{}\n".format(key, ', '.join(map(str, value)))
                    else:
                        info += "{}:{}\n".format(key,value)
            experiment_info = info
            experiment_result = ExperimentResult(info = experiment_info,results_path = '')
            experiment_result.save()
            relative_path = 'testing/results/graph'+str(experiment_result.pk)+'.pdf'
            graph_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
                                      'uploads/'+relative_path)
            result.savefig(graph_path)
            plt.close(result)
            experiment_result.results_path = relative_path
            experiment_result.save()
            return redirect(experiment_result)
    else:
        form = TestingForm()
        return render(request, 'algotesting/test.html', {'form': form})

class TestResult(DetailView):
    model = ExperimentResult
    template_name = 'algotesting/test_results.html'

