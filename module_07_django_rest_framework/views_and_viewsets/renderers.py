import csv
import io
from rest_framework.renderers import BaseRenderer


class CSVRenderer(BaseRenderer):
    """Render API response as CSV download."""
    media_type = "text/csv"
    format = "csv"

    def render(self, data, accepted_media_type=None, renderer_context=None):
        if not data:
            return ""

        if isinstance(data, dict) and "results" in data:
            data = data["results"]

        if not isinstance(data, list):
            data = [data]

        output = io.StringIO()
        writer = csv.DictWriter(output, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)
        return output.getvalue()


# Usage in ViewSet:
# from rest_framework.renderers import JSONRenderer, BrowsableAPIRenderer
#
# class MarketViewSet(viewsets.ModelViewSet):
#     renderer_classes = [JSONRenderer, BrowsableAPIRenderer, CSVRenderer]
#     # GET /api/markets/?format=csv