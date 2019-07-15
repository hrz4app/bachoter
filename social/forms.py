from django import forms
from django.core.files.images import get_image_dimensions

from location_field.forms.plain import PlainLocationField

from .models import BachText, BachPicture, BachLocation, BachListening

class TextForm(forms.ModelForm):
    class Meta:
        model = BachText
        fields = ('text',)
        widgets = {
            'text': forms.Textarea(attrs={
                'cols': 40,
                'rows': 3,
                'placeholder': u'Write bachot here...',
                'style': 'resize:none'}),
        }

    def __init__(self, *args, **kwargs):
        super(TextForm, self).__init__(*args, **kwargs)
        self.fields['text'].label = False

class PictureForm(forms.ModelForm):
    class Meta:
        model = BachPicture
        fields = ('caption', 'picture',)
        widgets = {
            'caption': forms.Textarea(attrs={
                'cols': 40,
                'rows': 3,
                'placeholder': u'Write caption here...',
                'style': 'resize:none'}),
            'picture': forms.FileInput(),
        }

    def __init__(self, *args, **kwargs):
        super(PictureForm, self).__init__(*args, **kwargs)
        self.fields['caption'].label = False
        self.fields['picture'].label = False
    
    def clean_picture(self):
        picture = self.cleaned_data['picture']
        try:
            img_name, extension = picture.content_type.split('/')
            if not extension in ['jpeg', 'jpg', 'pjpeg', 'gif', 'png']:
                print('not png jpg')
                raise forms.ValidationError(u"Please use a JPG, JPEG, GIF or PNG extension.")
        except AttributeError:
            pass
        return picture

class LocationForm(forms.ModelForm):
    class Meta:
        model = BachLocation
        fields = ('caption', 'name', 'picture', 'city', 'location',)
        widgets = {
            'caption': forms.Textarea(attrs={
                'cols': 40,
                'rows': 3,
                'placeholder': u'Write caption here...',
                'style': 'resize:none'}),
            'city': forms.TextInput(attrs={
                'placeholder': u'Name of city, district, or sub-district, street...'}),
            'name': forms.TextInput(attrs={
                'placeholder': u'Name of place...'}),
            'location': PlainLocationField(),
            'picture': forms.FileInput(),
        }

    def __init__(self, *args, **kwargs):
        super(LocationForm, self).__init__(*args, **kwargs)
        self.fields['caption'].label = False
        self.fields['city'].label = False
        self.fields['name'].label = False
        self.fields['location'].label = False
        self.fields['picture'].label = False
    
    def clean_picture(self):
        picture = self.cleaned_data['picture']
        try:
            img_name, extension = picture.content_type.split('/')
            if not extension in ['jpeg', 'jpg', 'pjpeg', 'gif', 'png']:
                print('not png jpg')
                raise forms.ValidationError(u"Please use a JPG, JPEG, GIF or PNG extension.")
        except AttributeError:
            pass
        return picture

class ListeningForm(forms.ModelForm):
    class Meta:
        model = BachListening
        fields = ('track_title', 'caption',)
        widgets = {
            'track_title': forms.TextInput(attrs={
                'id': 'searching-track',
                'placeholder': u'Track Title...'}),
            'caption': forms.Textarea(attrs={
                'cols': 40,
                'rows': 3,
                'placeholder': u'Write caption here...',
                'style': 'resize:none'}),
        }

    def __init__(self, *args, **kwargs):
        super(ListeningForm, self).__init__(*args, **kwargs)
        self.fields['track_title'].label = False
        self.fields['caption'].label = False