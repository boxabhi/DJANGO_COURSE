from rest_framework.validators import ValidationError




def no_numbers(value):
    if any(char.isdigit() for char in value):
        raise ValidationError("Name should not contain numbers")
    
def business_email(value):
    if value.split('@')[1] == "gmail.com":
        raise ValidationError("Email must be a business email")

    

