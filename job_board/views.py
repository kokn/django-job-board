from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.template.loader import select_template
from django.contrib.formtools.preview import FormPreview
from django.views.generic import list_detail

from job_board.models import *
from job_board.forms import *

queryset = Job.objects.filter()

template_object_name = 'job'

extra_context = {'base_template' : 'base.html'}

def job_list(request):
    job_list_template = (
        "job_board/list.html",
        "job_board/job_list.html",
    )

    template = select_template(job_list_template) # returns Template object
    template_name = template.name

    paginate_by = 10
    
    return list_detail.object_list(request, queryset,
                                    paginate_by = paginate_by,
                                    template_name = template_name,
                                    extra_context = extra_context,
                                    template_object_name = template_object_name)

def job_detail(request, slug=None, object_id=None):
    job_detail_template = (
        "job_board/view.html",
        "job_board/detail.html",
        "job_board/job_detail.html",
    )

    template = select_template(job_detail_template)
    template_name = template.name

    return list_detail.object_detail(request, queryset,
                                     object_id = object_id,
                                     slug = slug,
                                     template_name = template_name,
                                     extra_context = extra_context,
                                     template_object_name = template_object_name)

class JobFormPreview(FormPreview):
    preview_template = 'job_board/preview.html'
    form_template = 'job_board/form.html'
        
    def done(self, request, cleaned_data):
        form = JobForm(request.POST)
        job = form.save()

        message = """Your job posting has been saved successfully. Thank you very much.
        """

        request.notifications.create(message, 'success')

        params = {'slug': job.slug, 'object_id': job.id}
        return HttpResponseRedirect(reverse('job-detail', kwargs=params))