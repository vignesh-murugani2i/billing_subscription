from rest_framework import viewsets
from rest_framework.response import Response

from plan.models import Plan
from plan.serializer import PlanSerializer


class PlanViewSet(viewsets.ModelViewSet):
    """This class provides all the CRUD functionalities for Plan Model"""

    serializer_class = PlanSerializer
    queryset = Plan.objects.all()

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        print(instance)
        self.perform_destroy(instance)
        return Response(f"Plan id {self.kwargs.get('pk')} deleted")
