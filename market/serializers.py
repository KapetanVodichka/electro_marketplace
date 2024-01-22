from rest_framework import serializers
from .models import NetworkElement, Product, Contacts


class ContactsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contacts
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class NetworkElementSerializer(serializers.ModelSerializer):
    contacts = ContactsSerializer()
    products = ProductSerializer(many=True, source='product_set')

    class Meta:
        model = NetworkElement
        fields = ['id', 'name', 'level', 'supplier', 'debt_to_supplier', 'contacts', 'products']


class CreateNetworkElementSerializer(serializers.ModelSerializer):
    contacts = ContactsSerializer()
    products = ProductSerializer(many=True, write_only=True)

    class Meta:
        model = NetworkElement
        fields = ['id', 'name', 'level', 'supplier', 'debt_to_supplier', 'contacts', 'products']

    def create(self, validated_data):
        contacts_data = validated_data.pop('contacts')
        products_data = validated_data.pop('products')
        network_element = NetworkElement.objects.create(**validated_data)

        contact = Contacts.objects.create(network_element=network_element, **contacts_data)
        contact.save()

        for product_data in products_data:
            product = Product.objects.create(network_element=network_element, **product_data)
            product.save()

        return network_element
