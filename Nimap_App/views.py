from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Client, Project
from .serializers import *
from rest_framework import generics
from django.utils import timezone

class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class1=ClientSerializer1
    serializer_class = ClientSerializer
    permission_classes = [IsAuthenticated]
    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return self.serializer_class1  # Use ClientSerializer1 for PUT/PATCH
        return self.serializer_class
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
    def retrieve(self, request, *args, **kwargs):
        """Custom logic for retrieving client details along with associated projects."""
        # Get the client object by its primary key (ID)
        client = self.get_object()

        # Serialize the client data (excluding the projects)
        serializer = self.get_serializer(client)
        data = serializer.data

        # Add custom logic to include associated projects
        projects_data = [
            {"id": project.id, "name": project.project_name}
            for project in client.projects.all()
        ]
        
        # Reorder the fields in the desired order
        data = {
            "id": data["id"],
            "client_name": data["client_name"],
            "projects": projects_data,  # Insert projects here
            "created_at": data["created_at"],
            "created_by": data["created_by"],
            "updated_at": data.get("updated_at", data.get("created_at")) 
        }

        # Return the custom response
        return Response(data, status=status.HTTP_200_OK)
    def update(self, request, *args, **kwargs):
        """Handle PUT or PATCH request to update client information, including 'updated_at'."""
        partial = kwargs.pop('partial', False)  # Handle PATCH or PUT
        client = self.get_object()

        # Explicitly update the `updated_at` field
        request.data['updated_at'] = timezone.now().isoformat()

        # Get the appropriate serializer based on the method
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(client, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)

        # Perform the update
        self.perform_update(serializer)

        # Now get the updated client and its related projects
        client = serializer.instance  # Get the updated client object

        # Serialize the projects related to the client
        # projects_data = ProjectSerializer(client.projects.all(), many=True).data

        # Prepare the response data
        response_data = {
            'id': client.id,
            'client_name': client.client_name,
            'created_at': client.created_at.isoformat(),
            'created_by': client.created_by.username,  # Assuming `created_by` is a User object
            'updated_at': client.updated_at.isoformat(),
            # 'projects': projects_data,  # Include the projects
        }

        # Return the response with the formatted data
        return Response(response_data, status=status.HTTP_200_OK)
    def delete(self, request, *args, **kwargs):
        client = self.get_object()
        client.delete()
        return Response({"message": f"Client with ID {client.id} has been successfully deleted."}, status=204)

class ClientDetailAPIView(generics.RetrieveAPIView):
    queryset = Client.objects.prefetch_related('projects')  # Prefetch related projects for efficiency
    serializer_class = ClientSerializer1
    permission_classes = [IsAuthenticated]

class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request):
        user = request.user.id  # Get the logged-in user
        queryset = Project.objects.filter(created_by_id=user)
        serializer = CustomProjectSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request, client_pk=None):
        user = request.user.id  # Get the logged-in user's ID
        
        # Retrieve the client using the client_pk provided in the URL
        try:
            client = Client.objects.get(id=client_pk)
        except Client.DoesNotExist:
            return Response({"detail": "Client not found."}, status=status.HTTP_404_NOT_FOUND)
        
        # Get the project name and users from the request data
        project_name = request.data.get('project_name')
        users_data = request.data.get('users', [])
        if not users_data:
            return Response({"detail": "At least one user is required."}, status=status.HTTP_400_BAD_REQUEST)

        # Create the new project and associate it with the client and the logged-in user
        project = Project.objects.create(
            project_name=project_name,
            client=client,
            created_by=request.user
        )

        # Add users to the project
        for user_data in users_data:
            try:
                # Assuming user_data has 'id' and 'name' for matching the user
                user = User.objects.get(id=user_data['id'], username=user_data['name'])
                project.users.add(user)
            except User.DoesNotExist:
                return Response({"detail": f"User with ID {user_data['id']} and name {user_data['name']} not found."}, status=status.HTTP_404_NOT_FOUND)

        # Save the project after adding users
        project.save()

        # Custom response format
        response_data = {
            'id': project.id,
            'project_name': project.project_name,
            'client': project.client.client_name,  # Return the client name
            'users': [{'id': user.id, 'name': user.username} for user in project.users.all()],
            'created_at': project.created_at.isoformat(),
            'created_by': project.created_by.username  # Return the username of the creator
        }

        # Return the response with the formatted data
        return Response(response_data, status=status.HTTP_201_CREATED)
