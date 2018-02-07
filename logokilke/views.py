from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.shortcuts import render, render_to_response, redirect, HttpResponse, HttpResponseRedirect
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.decorators import method_decorator
from django.template import RequestContext

from logokilke.models import *
from logokilke.forms import *
from logokilke.scripts import logofy
from logokilke.scripts import add_logo
from logokilke.scripts import save_dir
from logokilke.scripts import logo_dir
from logokilke.scripts import logo_list

from PIL import Image
from io import StringIO

class IndexView(TemplateView):
    template_name = 'index.html'

class PrivateView(LoginRequiredMixin, TemplateView):
    """
    Login required to access this view
    """
    login_url = '/login/'
    redirect_field_name = 'next'
    template_name = 'private.html'


def index(request):
    """
    Index page
    """
    # Highlights the navbar
    active = 'index'
    return render_to_response('index.html', {
        'page_var': active,
    })

def single(request):
    """
    View for adding logos on one image
    """
    # Highlights the navbar
    active = 'single'

    # Gets the input form
    form = ImageUploadForm(request.POST, request.FILES)

    return render(request, 'single.html', {
        'page_var': active,
        'form': form,
    })

def multi(request):
    """
    View for adding logo on multiple image
    """
    # Highlights the navbar
    active = 'multi'
    return render(request, 'multi.html', {
    'page_var': active,
    })


"""
View taking in the form with images
"""
def upload_pic(request):
    # Highlights the navbar
    if not request.method=='POST':
        return HttpResponseForbidden('Allowed only via POST')

    active = 'single'
    form = ImageUploadForm(request.POST, request.FILES)

    if form.is_valid():
        """ Do the image stuff """
        corners = [3]
        img_file = request.FILES['image_field']
        pil_img = [Image.open(img_file)]
        logos = []
        for logo_name in logo_list:
            logos.append(Image.open(logo_dir+logo_name))

        b64_images = logofy(pil_img, logos, corners, quality_level=95)
        return render(request, 'single_output.html', {
            'page_var': active,
            'b64_images': b64_images,
            })
    return HttpResponseForbidden('Invalid form. Please try again.')
