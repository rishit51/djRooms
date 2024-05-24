from drf_spectacular.utils import extend_schema,OpenApiParameter
from drf_spectacular.types import OpenApiTypes

from .serializers import ChannelSerializer,ServerSerializer


server_list_docs=extend_schema(
    responses=ServerSerializer(many=True),
    parameters=[
        OpenApiParameter(
            name="category",
            type=OpenApiTypes.STR
        ),
        OpenApiParameter(
            name="with_num_mem",
            type=OpenApiTypes.BOOL
        )
        ,OpenApiParameter(
            name="by_server_id",
            type=OpenApiTypes.INT
        )
        ,OpenApiParameter(
            name="by_user",
            type=OpenApiTypes.BOOL
        )
        ]
)