from django import forms


class FavoriteForm(forms.Form):
    character_id = forms.IntegerField(widget=forms.HiddenInput())


class LikeForm(forms.Form):
    character_id = forms.IntegerField(widget=forms.HiddenInput())


class RemoveFavoriteForm(forms.Form):
    character_id = forms.IntegerField(widget=forms.HiddenInput())


class RemoveLikeForm(forms.Form):
    character_id = forms.IntegerField(widget=forms.HiddenInput())
