import os
from drf_yasg.generators import OpenAPISchemaGenerator


class APISchemeGenerator(OpenAPISchemaGenerator):
    def get_schema(self, request=None, public=False):
        schema = super().get_schema(request, public)
        schema.base_path = os.path.join(schema.base_path, 'api-v2/')
        return schema
