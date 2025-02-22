from django.shortcuts import render, get_object_or_404

from .models import *
from django.http import JsonResponse


def post_list(request):
    posts = Post.objects.all().order_by('-id')
    return render(request, 'post_list.html', {'posts' : posts})


def post_detail(request, post_id):
    post = Post.objects.get(id = post_id)
    comments = Comment.objects.filter(post = post, parent=None).order_by('-id')
    return render(request, 'post_detail.html', {
        'post' : post,
        'comments' : comments
    })

def add_comment(request):
    if request.method == "POST":
        content = request.POST.get('content')
        parent_id = request.POST.get('parent_id')
        post_id = request.POST.get('post_id')

        parent = get_object_or_404(Comment,id=parent_id) if parent_id else None
        post = get_object_or_404(Post, id = post_id)
        comment = Comment.objects.create(
            content = content, parent = parent, post=post
        )
        return JsonResponse({
            'id' : comment.id,
            'content': content
        })


from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import ResumeSerializer, JobDescriptionSerializer
from .models import Resume, JobDescription
from .analyzer import process_resume
import sys, os

class JobDescriptionAPI(APIView):
    def get(self , request):
        queryset  = JobDescription.objects.all()
        serializer = JobDescriptionSerializer(queryset, many = True) 
        return Response({
                'status' : True,
                'message' : 'data',
                'data' : serializer.data
            })

class ResumeAPI(APIView):
    def post(self , request):  # sourcery skip: extract-method
        try:
            data = request.data
            if not data.get('job_description'):
                return Response({
                    'status' : False,
                    'message' : 'missing job_description',
                    'data' : {}
                })
            serializer = ResumeSerializer(data = data)
            if not serializer.is_valid():
                return Response({
                    'status' : False,
                    'message' : 'missing fields',
                    'data' : serializer.errors
                })

            serializer.save()
            _data = serializer.data
            resume_instance = Resume.objects.get(id=_data['id'])  # Fetch the instance
            resume_path = resume_instance.resume.path  # Get the full file path
            final_data = process_resume(resume_path,
                    JobDescription.objects.get(id = data.get('job_description')).id)

            return Response({
                'status' : True,
                'data' : final_data
            })
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            print(e)
            return Response({})