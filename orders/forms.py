
from django import forms


class CheckoutForm(forms.Form):
    shipping_address = forms.CharField(
        label="Delivery Address",
        widget=forms.Textarea(attrs={"rows": 3, "class": "form-control"}),
        min_length=10,
        max_length=1000,
    )
    phone = forms.CharField(
        label="Phone Number",
        max_length=20,
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )

    def clean_shipping_address(self):
        address = self.cleaned_data["shipping_address"].strip()
        if len(address) < 10:
            raise forms.ValidationError("Please enter a complete delivery address.")
        return address

    def clean_phone(self):
        phone = self.cleaned_data["phone"].strip()
        digits = "".join(character for character in phone if character.isdigit())

        if len(digits) < 10 or len(digits) > 15:
            raise forms.ValidationError(
                "Enter a valid phone number containing 10 to 15 digits."
            )

        return phone
