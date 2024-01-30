from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View

from site_module.models import SiteSettings
from .forms import ContactUsForms, ContactUsModelForm, ProfileImageForm
from django.views.generic.edit import FormView, CreateView
from django.views.generic import ListView
from .models import ProfileImage, ContactUs


class ContactUsView(FormView):
    template_name = 'contact_module/contact_page.html'
    form_class = ContactUsModelForm
    success_url = '/'

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        settings = SiteSettings.objects.filter(is_main_setting=True).first()
        context['settings'] = settings
        return context


class CreateProfile(CreateView):
    template_name = 'contact_module/create_profile.html'
    model = ProfileImage
    fields = '__all__'
    success_url = '/contact-us/create-profile'

    # def get(self, request):
    #     form = ProfileImageForm()
    #     return render(request, 'contact_module/create_profile.html', {'form': form})
    #
    # def post(self, request):
    #     submitted_form = ProfileImageForm(request.POST, request.FILES)
    #     if submitted_form.is_valid():
    #         profile_image = ProfileImage(profile_image=request.FILES['profile_image'])
    #         profile_image.save()
    #         return redirect(reverse('create_profile'))
    #     return render(request, 'contact_module/create_profile.html', {'form': submitted_form})


class ProfileViews(ListView):
    model = ProfileImage
    template_name = 'contact_module/profiles.html'
    context_object_name = 'profiles'



def contact_page(request):
    if request.method == 'POST':
        # contact_form = ContactUsForms(request.POST)
        contact_form = ContactUsModelForm(request.POST)
        if contact_form.is_valid():
            # contact_us = ContactUs(
            #     title=contact_form.cleaned_data.get('title'),
            #     full_name=contact_form.cleaned_data.get('full_name'),
            #     email=contact_form.cleaned_data.get('email'),
            #     message=contact_form.cleaned_data.get('message')
            # )
            # contact_us.save()
            contact_form.save()
            return redirect(reverse('index_page'))
    # contact_form = ContactUsForms()
    contact_form = ContactUsModelForm()
    return render(request, 'contact_module/contact_page.html', {'contact_form': contact_form})
