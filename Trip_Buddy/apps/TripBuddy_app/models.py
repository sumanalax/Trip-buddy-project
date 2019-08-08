from django.db import models
import re, bcrypt

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9+-_.]+\.[a-zA-Z]+$')

class UserManager(models.Manager):
    def register(self, form_data):
        # print("inside of your madels!!!", form_data)
        errors = []

        if len (form_data["first_name"]) < 1:
            errors.append("First Name is required")
        elif len(form_data["first_name"]) < 2:
            errors.append("First Name must be letters or longer")

        if len(form_data["last_name"]) < 1:
            errors.append("Last Name is required")
        elif len(form_data["last_name"]) < 2:
            errors.append("Last Name must be letters or longer")

        if len(form_data["e-mail"]) < 1:
            errors.append("e-mail is required")
        elif not EMAIL_REGEX.match(form_data["e-mail"]):
            errors.append("Invalid Email")
        else:
            if len(User.objects.filter(email=form_data["e-mail"].lower())) > 0:
                errors.append(" E-mail is registered with a another account")

        if len(form_data["password"]) < 1:
            errors.append("Password is required")
        elif len(form_data["password"]) < 8:
            errors.append("Password must be 8 letters or longer")

        if len(form_data["confirm_password"]) < 1:
            errors.append("Confirm Password is required")
        elif form_data["confirm_password"] != form_data["confirm_password"]:
            errors.append("Confirm Password should match Password")

        if len(errors) == 0:
            hashed_pw = bcrypt.hashpw(form_data["password"].encode(), bcrypt.gensalt())
            user =  User.objects.create(
                first_name = form_data["first_name"],
                last_name = form_data["last_name"],
                email = form_data["e-mail"].lower(),
                password = (hashed_pw)
            )
            return(True, user)
        else:
            return(False, errors)  

    def login(self,form_data):

        errors = []

        if len(form_data["e-mail"]) < 1:
            errors.append("e-mail is required")
        elif not EMAIL_REGEX.match(form_data["e-mail"]):
            errors.append("Invalid Email")
        else:
            if len(User.objects.filter(email=form_data["e-mail"].lower())) == 0:
                errors.append("Unknown email {}".format(form_data["e-mail"]))

        if len(form_data["password"]) < 1:
            errors.append("password is required")
        elif len(form_data["password"]) < 8:
            errors.append("password must be 8 letters or longer") 
        
        if len(errors) > 0:
            return(False, errors)

        user = User.objects.filter(email=form_data["e-mail"].lower())
        hashed_pw = user.first().password

        if bcrypt.checkpw(form_data["password"].encode(), hashed_pw.encode()):
            return(True, user)
        else:
            errors.append("Incorrect password")
            return(False, errors)


class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updtaed_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

class TravelTripManager(models.Manager):
    def savetrip(self, form_data):
        user_id = User.objects.get(id=form_data['user_id'])
        traveltrip = TravelTrip.objects.create(
                destination = form_data["destination"],
                description = form_data["description"],
                travel_date_from = form_data["travel_date_from"],
                travel_date_to = form_data["travel_date_to"],
                user_id = user_id
                )
        return(True, traveltrip)

class TravelTrip(models.Model):
    destination = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    travel_date_from  = models.DateField(auto_now_add=True)
    travel_date_to = models.DateField(auto_now=True)
    user_id = models.ForeignKey(User)

    objects = TravelTripManager()
