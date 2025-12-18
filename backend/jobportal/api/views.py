from rest_framework import viewsets, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User
from .models import Job, JobApplication
from .serializers import JobSerializer, JobApplicationSerializer
from django.contrib.auth import get_user_model
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.exceptions import MethodNotAllowed




# Existing ViewSets
class JobViewSet(viewsets.ModelViewSet):
    queryset = Job.objects.all()
    serializer_class = JobSerializer
    permission_classes = [permissions.IsAuthenticated]


class JobApplicationViewSet(viewsets.ModelViewSet):
    queryset = JobApplication.objects.all()
    serializer_class = JobApplicationSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        raise MethodNotAllowed("POST", detail="Use /applications/apply/ instead")

    @action(detail=False, methods=["post"])
    def apply(self, request):
        job_id = request.data.get("job_id")

        if not job_id:
            return Response({"detail": "job_id is required"}, status=400)

        job = Job.objects.filter(id=job_id).first()
        if not job:
            return Response({"detail": "Job not found"}, status=404)

        user = User.objects.first()
        if not user:
            return Response(
                {"detail": "No user exists. Create a user in admin."},
                status=400
            )

        if JobApplication.objects.filter(job=job, user=user).exists():
            return Response({"detail": "Already applied"}, status=400)

        JobApplication.objects.create(job=job, user=user)
        return Response({"detail": "Applied successfully"}, status=201)






        
   

User = get_user_model()
# New Registration API
class RegisterView(APIView):
    def post(self, request):
        try:
            username = request.data.get("username")
            password = request.data.get("password")
            role = request.data.get("role")  # optional

            if not username or not password:
                return Response({"detail": "Username and password are required"}, status=400)

            if User.objects.filter(username=username).exists():
                return Response({"detail": "Username already exists"}, status=400)

            # Create user using the custom User model
            user = User.objects.create_user(username=username, password=password, role=role)
            user.save()

            return Response({"detail": "User registered successfully"}, status=201)

        except Exception as e:
            return Response({"detail": str(e)}, status=500)
