from django import forms
from django.contrib.auth.models import User
from django.core.files.images import get_image_dimensions

from authentication.validators import ForbiddenUsernamesValidator, UniqueEmailEditValidator
from authentication.models import Profile

class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'email',)

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        super(UserEditForm, self).__init__(*args, **kwargs)
        self.fields['username'].validators.append(ForbiddenUsernamesValidator)
        self.fields['email'].validators.append(UniqueEmailEditValidator(self.request.user.email))

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('name', 'facebook', 'twitter', 'instagram', 'bio',)

class ProfilePictureForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('picture',)
        widgets = {
            'picture': forms.FileInput()
        }

    def __init__(self, *args, **kwargs):
        super(ProfilePictureForm, self).__init__(*args, **kwargs)
        self.fields['picture'].label = False

    def clean_picture(self):
        picture = self.cleaned_data['picture']
        try:
            width, height = get_image_dimensions(picture)
            max_width = max_height = 720
            if width > max_width or height > max_height:
                raise forms.ValidationError(u"Please use an image that is %s x %s pixels or smaller." % (max_width, max_height))
            img, extension = picture.content_type.split('/')
            if not extension in ['jpeg', 'jpg', 'pjpeg', 'gif', 'png']:
                raise forms.ValidationError(u"Please use a JPG, JPEG, GIF or PNG extension.")
            if len(picture) > (3000 * 1024):
                raise forms.ValidationError(u"Avatar file size may not exceed 3Mb.")
        except AttributeError:
            pass
        return picture