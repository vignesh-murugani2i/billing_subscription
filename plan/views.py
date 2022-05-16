from rest_framework import viewsets

from plan.models import Plan
from plan.serializer import PlanSerializer


class PlanViewSet(viewsets.ModelViewSet):
    """This class provides all the CRUD functionalities for Plan"""

    serializer_class = PlanSerializer
    queryset = Plan.objects.all()
