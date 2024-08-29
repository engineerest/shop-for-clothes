from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from Landing.contact.serializers import ContactSerializer
from Landing.core.models import *


class ContactViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)
    serializer_class = ContactSerializer
    queryset = Seller.objects.all()

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    # def get_seller_info(self, serializer, request):
    #     serializer_seller = ContactSerializer(Seller.objects.filter(user=self.request.user), many=True)
    #     seller_payload = {
    #         'seller': serializer_seller.data,
    #         'email': serializer.data['email'],
    #         'phone': serializer.data['phone'],
    #         'address': serializer.data['address'],
    #         'city': serializer.data['city'],
    #         'country': serializer.data['country'],
    #     }
    #     serializer_seller.save(seller_payload)
    #
    #     return Response(seller_payload, status=status.HTTP_200_OK)




