from rest_framework import viewsets
from .models import Server
from .serializer import ServerSerializer
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError, AuthenticationFailed
from django.db.models import Count
from .schema import server_list_docs


class ServerListViewSet(viewsets.ViewSet):
    queryset = Server.objects.all()

    @server_list_docs
    def list(self, request):
        """
        Retrieves a list of servers based on the provided filters.

        This method allows filtering servers based on different criteria such as category,
        quantity, user, server ID, and the option to include the number of members in each server.

        Parameters:
            - request (HttpRequest): The HTTP request object.

        Returns:
            - Response: An HTTP response containing a list of serialized servers.

        Raises:
            - AuthenticationFailed: If the user is not authenticated and tries to filter by user or server ID.
            - ValidationError: If the server ID provided in the 'by_serverid' parameter is not found.

        Examples:
            - GET /servers/?category=network&qty=10&by_user=true&with_num_members=true
                - Retrieves a list of up to 10 servers in the 'network' category that belong to the authenticated user,
                  including the number of members in each server.

            - GET /servers/?by_serverid=12345
                - Retrieves the server with the ID '12345' if it exists.

        Note:
            - The 'category' parameter filters servers by their category name.
            - The 'qty' parameter limits the number of servers returned.
            - The 'by_user' parameter filters servers by the authenticated user.
            - The 'with_num_members' parameter includes the count of members in each server.
            - The 'by_serverid' parameter filters servers by their specific server ID.
              If no server is found with the provided ID, a ValidationError is raised.
        """
        category = request.query_params.get("category")
        qty = request.query_params.get("qty")
        by_user = request.query_params.get("by_user") == "true"
        by_serverid = request.query_params.get("by_serverid")
        with_num_members = request.query_params.get("with_num_members") == "true"

        # if by_user or by_serverid and not request.user.is_authenticated:
        #     raise AuthenticationFailed()

        if category:
            self.queryset = self.queryset.filter(category__name=category)

        if by_user:
            if by_user and request.user.is_authenticated:
                user_id = request.user.id
                self.queryset = self.queryset.filter(member=user_id)
            raise AuthenticationFailed()

        if qty:
            self.queryset = self.queryset[: int(qty)]

        if with_num_members:
            self.queryset = self.queryset.annotate(num_members=Count("member"))

        if by_serverid:
            if by_user and request.user.is_authenticated:
                try:
                    self.queryset = self.queryset.filter(id=by_serverid)
                    if not self.queryset.exists():
                        raise ValidationError(detail=f"Server with id {by_serverid} not found")
                except ValidationError:
                    raise ValidationError(detail="Server value error")
            raise AuthenticationFailed()

        serializer = ServerSerializer(self.queryset, many=True, context={"num_members": with_num_members})
        return Response(serializer.data)
