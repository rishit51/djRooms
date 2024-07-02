from drf_spectacular.utils import extend_schema,OpenApiParameter
from drf_spectacular.types import OpenApiTypes

from .serializers import AccountSerializer


user_doc=extend_schema(
    responses=AccountSerializer(many=False),
    parameters=[
        OpenApiParameter(
            name="user_id",
            type=OpenApiTypes.INT,
            description="User Id"
        )
        ]
)
