from django.shortcuts import render

# Create your views here.

from rest_framework.viewsets import ViewSet
from .models import Server
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError,AuthenticationFailed
from .serializers import ServerSerializer
from django.db.models import Count
from .schema import server_list_docs

class ServerListViewSet(ViewSet):        
    queryset=Server.objects.all()
    @server_list_docs
    def list(self, request):
        """
    List servers based on various query parameters.

    This method filters and annotates the queryset of servers based on query parameters 
    provided in the request. The following filters are supported:
    
    - `by_user`: Filters servers where the current user is a member. Requires user authentication.
    
    - `by_server_id`: Filters servers by a specific server ID.
    - `category`: Filters servers by a specific category name.
    - `with_num_mem`: Annotates each server with the number of members if set to "true".
    
    Parameters:
    - request: The HTTP request object containing query parameters.

    Raises:
    - AuthenticationFailed: If `by_user` or `by_server_id` is set and the user is not authenticated.
    - ValidationError: If `by_server_id` is provided but does not exist or is not a valid ID.

    Returns:
    - Response: A Response object containing serialized data of the filtered servers.
    
    Examples:
        
        Example 1: Filter servers by category
            GET /api/servers?category=gaming
            # response will contain servers in the 'gaming' category

        Example 2: Filter servers by user membership
            GET /api/servers?by_user=true
            Headers: Authorization: Bearer <token>
            # response will contain servers where the authenticated user is a member

        Example 3: Filter servers by server ID
            GET /api/servers?by_server_id=12345
            # response will contain the server with ID 12345

        Example 4: Annotate servers with number of members
            GET /api/servers?with_num_mem=true
            # response will contain servers annotated with the number of members
    
        """
        by_user=request.query_params.get('by_user') == "true"
        
        by_server_id=request.query_params.get('by_server_id')      
        category=request.query_params.get("category")
        with_num_mem=request.query_params.get('with_num_mem') == "true"
        if category:
            self.queryset=self.queryset.filter(category__name=category)
        if (by_user or by_server_id) and not request.user.is_authenticated:
            raise AuthenticationFailed(detail="Incorrect authentication credentials",code=401)
        if by_user:
            user_id=request.user.id
            self.queryset=self.queryset.filter(members=user_id)
        
        if with_num_mem:
            self.queryset=self.queryset.annotate(num_members=Count("members"))
        if by_server_id:
            try:
                self.queryset=self.queryset.filter(id=by_server_id)
                if not self.queryset.exists():
                    raise ValidationError(detail=f"Server with id {by_server_id} not exists")
            except ValueError:
                raise ValidationError(detail='',)

        serializer=ServerSerializer(self.queryset,many=True,context={"with_num_members":with_num_mem})
        return Response(serializer.data)

