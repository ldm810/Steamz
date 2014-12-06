from django import forms            
from django.contrib.auth.models import User   # fill in custom user info then save it 
from django.contrib.auth.forms import UserCreationForm 
from steam.models import Profile

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required = True)
    first_name = forms.CharField(required = True)
    last_name = forms.CharField(required = True)
    year = forms.IntegerField(required = True)
    preference = forms.CharField(max_length=1, required=True)
    gender = forms.CharField(max_length=1, required=True)
    #school_key = forms.CharField(max_length=256, required=False)



    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')        

    def save(self,commit = True):   
        user = super(RegistrationForm, self).save(commit = False)

        


        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.year = self.cleaned_data['year']
        user.preference = self.cleaned_data['preference']
        user.gender = self.cleaned_data['gender']

        if commit:
        	user.save()

        new_person = Profile(user=user, first_name=user.first_name, 
        	last_name=user.last_name, year=user.year, email=user.email, 
        	preference=user.preference, gender=user.gender,voter_score=0)


        if commit:
            new_person.save()

        return user
