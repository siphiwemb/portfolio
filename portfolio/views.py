from django.http.response import JsonResponse
from django.shortcuts import redirect, render
from .models import (User, Profile)
from .forms import (ProfileForm, UserForm, LoginForm)
from django.contrib.auth import authenticate, login
from .portfolio_objects import DictObj
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout

create_dict = DictObj()

def sign_in(request):
    login_form = LoginForm(request.POST or None)
    context = create_dict.get_dict(login_form=login_form, title='Sign In', action='/portfolio/')

    if request.method == "POST":
        if login_form.is_valid():
            username = login_form.cleaned_data.get('username')
            password = login_form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                user_qs = User.objects.filter(username=username).values()
                user_id = user_qs[0]['id']
                request.session.set_expiry(86400) #session expires after a day
                login(request, user)
                return redirect('/portfolio/home/'+str(user_id)+'/')
            else:
                context['error'] = 'Please enter the correct username and password. Note that both fields may be case-sensitive.'
                return render(request, 'portfolio/sign_in.html', context)

    else:
        return render(request, 'portfolio/sign_in.html', context)


@login_required(login_url='/portfolio/')
def home(request, id):
    if is_current_user_id(request, id):
        context = create_dict.get_dict(id=str(id), title='home')
        return render(request, 'portfolio/home.html', context)
    else:
        logout(request)
        return redirect('/portfolio/')


@login_required(login_url='/portfolio/')
def display_user_profile_view(request, id):
    if is_current_user_id(request, id):
        user_qs = User.objects.filter(id=id).values("id", "username", "email", "first_name", "last_name")
        
        if len(user_qs) < 1:
            return redirect('/portfolio/')

        user_items = user_qs[0]
        personal = create_dict.get_dict(username=user_items["username"], name=user_items["first_name"], surname=user_items["last_name"])

        profile_obj = Profile.objects.filter(user=user_items['id'])
        address = None
        contact = None

        if profile_obj.exists():
            profile_qs = profile_obj.values("cellphone", "house_no", "street", "surburb", "city",
            "state", "latitude", "longitude")
            profile_items = profile_qs[0]

            street = profile_items["house_no"] + " " + profile_items["street"]
            address = create_dict.get_dict(street=street, surburb=profile_items["surburb"], 
                        city=profile_items["city"], state=profile_items["state"], latitude=profile_items["latitude"], longitude=profile_items["longitude"]
                    )

            contact = create_dict.get_dict(cellphone=profile_items["cellphone"], email=user_items["email"])
        else:
            address = create_dict.get_dict(house_no="", street="", surburb="", city="", state="", latitude="", longitude="")
            contact = create_dict.get_dict(cellphone="", email=user_items["email"])

        context = create_dict.get_dict(title="Profile", personal=personal, address=address, contact=contact, id=str(id))

        return render(request, "portfolio/profile.html", context)
    else:
        logout(request)
        return redirect('/portfolio/')


@login_required(login_url='/portfolio/')
def edit_user_profile(request, id):
    if is_current_user_id(request, id):
        try:
            user_instance = User.objects.get(id=id)
            user_form = UserForm(request.POST or None, instance=user_instance)
        except ObjectDoesNotExist:
            return redirect('/portfolio/')

        try:
            profile_instance = Profile.objects.get(user=user_instance)
            profile_form = ProfileForm(request.POST or None, instance=profile_instance)
        except ObjectDoesNotExist:
            profile_instance = None
            profile_form = ProfileForm(request.POST or None)

        context = create_dict.get_dict(title="Edit Profile", profile_form=profile_form, user_form=user_form, 
                action='/portfolio/edit-profile/'+str(id)+'/', id=str(id))
        

        if request.method == 'POST':
            if user_form.is_valid():
                user_form_instance = user_form.save(commit=False)
                user_form_instance.first_name = user_form.cleaned_data.get('first_name')
                user_form_instance.last_name = user_form.cleaned_data.get('last_name')
                user_form_instance.email = user_form.cleaned_data.get('email')
                user_form_instance.save()


            if profile_form.is_valid():
                profile_form_instance = profile_form.save(commit=False)

                if profile_instance is None:
                    profile_form_instance.user = user_instance
                else:
                    pass

                profile_form_instance.cellphone = profile_form.cleaned_data.get('cellphone')
                profile_form_instance.house_no = profile_form.cleaned_data.get('house_no')
                profile_form_instance.street = profile_form.cleaned_data.get('street')
                profile_form_instance.surburb = profile_form.cleaned_data.get('surburb')
                profile_form_instance.city = profile_form.cleaned_data.get('city')
                profile_form_instance.state = profile_form.cleaned_data.get('state')
                profile_form_instance.latitude = profile_form.cleaned_data.get('latitude')
                profile_form_instance.longitude = profile_form.cleaned_data.get('longitude')
                profile_form_instance.save()
            else:
                context["error"] = profile_form.errors
                return render(request, "portfolio/edit_profile.html", context)

            return redirect('/portfolio/profile/'+str(id)+'/')

        else:
            return render(request, "portfolio/edit_profile.html", context)
    else:
        logout(request)
        return redirect('/portfolio/')


@login_required()
def get_users(request):
    if request.method == 'GET':
        user_ids_list = User.objects.all().values_list("id", flat=True)
        profile_qs = Profile.objects.filter(user__in=user_ids_list).values("surburb", "city", "latitude", "longitude").order_by('user')
        user_qs = User.objects.all().values("username", "email", "first_name", "last_name").order_by('id')

        def link_user_to_profile(user, profile):
            user.update(profile)
            return user

        all_user_details_list = list(map(link_user_to_profile, user_qs, profile_qs))
        return JsonResponse(all_user_details_list, safe=False)
    else:
        return JsonResponse(list(), safe=False)


@login_required(login_url='/portfolio/')
def logout_user(request):
    logout(request)
    return redirect('/portfolio/')


def is_current_user_id(request, id):
    curr_user_id = request.user.id
    return curr_user_id == int(id)