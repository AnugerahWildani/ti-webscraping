from django import forms
from djcelery.models import PeriodicTask, IntervalSchedule, CrontabSchedule

class UpdateScheduleForm(forms.ModelForm):
    minute = forms.CharField(label='Minute', initial='*', widget=forms.TextInput(attrs={'class': 'form-control'}))
    hour = forms.CharField(label='Hour', initial='*', widget=forms.TextInput(attrs={'class': 'form-control'}))
    day_of_week = forms.CharField(label='Day', initial='*', widget=forms.TextInput(attrs={'class': 'form-control'}))
    day_of_month = forms.CharField(label='Day of Month', initial='*', widget=forms.TextInput(attrs={'class': 'form-control'}))
    month_of_year = forms.CharField(label='Month of Year', initial='*', widget=forms.TextInput(attrs={'class': 'form-control'}))
    class Meta:
        model = CrontabSchedule
        fields = ['minute', 'hour', 'day_of_week', 'day_of_month', 'month_of_year']
