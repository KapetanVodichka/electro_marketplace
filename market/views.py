from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, status
from rest_framework.response import Response

from .models import NetworkElement, Product, Contacts
from .permissions import IsActiveAndStaff
from .serializers import NetworkElementSerializer, ProductSerializer, ContactsSerializer, CreateNetworkElementSerializer


class NetworkElementViewSet(viewsets.ModelViewSet):
    queryset = NetworkElement.objects.all()
    serializer_class = NetworkElementSerializer
    permission_classes = [IsActiveAndStaff]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['contacts__country']

    def perform_update(self, serializer):
        # Запрет обновления поля "Задолженность перед поставщиком"
        instance = get_object_or_404(self.get_queryset(), pk=self.kwargs.get('pk'))
        serializer.save(debt_to_supplier=instance.debt_to_supplier)

    def create(self, request, *args, **kwargs):
        serializer = CreateNetworkElementSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        supplier = serializer.validated_data.get('supplier')

        # Проверка на максимальное количество уровней
        max_hierarchy_level = 2
        if supplier and supplier.level >= max_hierarchy_level:
            return Response(
                {
                    'detail': f'Нельзя добавить новый объект в сеть с максимальным уровнем иерархии '
                              f'({max_hierarchy_level}).'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Устанавливаем уровень иерархии в соответствии с логикой
        serializer.validated_data['level'] = supplier.level + 1 if supplier else 0
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get_queryset(self):
        queryset = super().get_queryset()
        country_filter = self.request.query_params.get('country', None)
        if country_filter:
            queryset = queryset.filter(contacts__country=country_filter)
        return queryset


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsActiveAndStaff]


class ContactsViewSet(viewsets.ModelViewSet):
    queryset = Contacts.objects.all()
    serializer_class = ContactsSerializer
    permission_classes = [IsActiveAndStaff]


class SupplierViewSet(viewsets.ModelViewSet):
    queryset = NetworkElement.objects.all()
    serializer_class = NetworkElementSerializer
    permission_classes = [IsActiveAndStaff]

    def get_queryset(self):
        queryset = super().get_queryset()
        country_filter = self.request.query_params.get('country', None)
        if country_filter:
            queryset = queryset.filter(contacts__country=country_filter)
        return queryset

    def perform_update(self, serializer):
        # Запрет обновления поля "Задолженность перед поставщиком"
        instance = get_object_or_404(self.get_queryset(), pk=self.kwargs.get('pk'))
        serializer.save(debt_to_supplier=instance.debt_to_supplier)
