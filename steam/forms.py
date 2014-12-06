from django import forms            
from django.contrib.auth.models import User   # fill in custom user info then save it 
from django.contrib.auth.forms import UserCreationForm 
from steam.models import Profile,Match

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required = True)
    first_name = forms.CharField(required = True)
    last_name = forms.CharField(required = True)
    year = forms.IntegerField(required = True)
    preference = forms.CharField(max_length=1, required=True)
    CHOICES = (('f', 'Female',), ('m', 'Male',))
    gender = forms.ChoiceField(widget=forms.RadioSelect, choices=CHOICES)
    preference = forms.ChoiceField(widget=forms.RadioSelect, choices=CHOICES)
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

        potential_matches = Profile.objects.filter(gender=user.preference).filter(preference=user.gender).exclude(user=user)
        for person in potential_matches:
            
            existing_match1 = Match.objects.filter(user1=person).filter(user2=new_person)
            existing_match2 = Match.objects.filter(user2=person).filter(user1=new_person)
            if (len(existing_match1) == 0 and len(existing_match2) ==0):
                new_match = Match(user1=person,user2=new_person)  
                

    # matches_for_user_2 = Match.objects.filter(user2=1)
        print 'potential matches', potential_matches
        return user



class MatchesForm(forms.Form):
    CHOICES = (('y', 'Yes',), ('n', 'No',))
    accept1 = forms.ChoiceField(widget=forms.RadioSelect, choices=CHOICES, help_text="Would you like to accept?")


    # An inline class to provide additional information on the form.
    class Meta:
        widgets = {'tag': forms.HiddenInput()}
    #     # Provide an association between the ModelForm and a model
    #     model = Match





