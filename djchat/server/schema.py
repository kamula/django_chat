from drf_spectacular.utils import extend_schema, OpenApiParameter
from drf_spectacular.types import OpenApiTypes
from .serializer import ServerSerializer, ChannelSerializer


server_list_docs = extend_schema(
    responses=ServerSerializer(many=True),
    parameters=[
        OpenApiParameter(
            name="category",
            type=OpenApiTypes.STR,
            location=OpenApiParameter.QUERY,
            description="Category of Servers to retrieve",
        ),
        OpenApiParameter(
            name="qty",
            type=OpenApiTypes.INT,
            location=OpenApiParameter.QUERY,
            description="Number of servers to retrieve",
        ),
        OpenApiParameter(
            name="by_user",
            type=OpenApiTypes.BOOL,
            location=OpenApiParameter.QUERY,
            description="Filter servers by the current authenticated user (True/False)",
        ),
        OpenApiParameter(
            name="with_num_members",
            type=OpenApiTypes.BOOL,
            location=OpenApiParameter.QUERY,
            description="Include the number of members for each server in the response (True/False)",
        ),
        OpenApiParameter(
            name="by_server_id",
            type=OpenApiTypes.INT,
            location=OpenApiParameter.QUERY,
            description="Filter servers by server id",
        ),
    ],
)
