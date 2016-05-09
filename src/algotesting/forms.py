from django import forms
from models import Dataset, Algorithm

class UploadAlgorithmFileForm(forms.ModelForm):
    class Meta:
        model = Algorithm
        fields = ['name', 'algorithm','description','train_parameters']

class QuickStartForm(forms.Form):
    base_capital = forms.FloatField(min_value= 0)
    stocks = forms.CharField()
    train_size = forms.FloatField(min_value=0.01, max_value=0.99)


class UploadDataFilesForm(forms.ModelForm):
    class Meta:
        model = Dataset
        fields = ['name','data', 'description', 'frequency', 'date_format']

class NameModelChoiceField(forms.ModelMultipleChoiceField):
    def label_from_instance(self, obj):
        return obj.name

class TestingForm(forms.Form):
    algorithm = NameModelChoiceField(queryset=Algorithm.objects)
    dataset = NameModelChoiceField(queryset=Dataset.objects)
    base_capital = forms.FloatField(min_value=0.0)
    stocks = forms.CharField()
    train_size = forms.FloatField(min_value=0.0, max_value=0.99)
    load_parameters = forms.BooleanField(required=False)
    save_parameters = forms.BooleanField(required=False)





