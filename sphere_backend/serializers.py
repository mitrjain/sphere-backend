from rest_framework import serializers

class LineItemSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)
    price = serializers.FloatField()
    quantity = serializers.IntegerField()
    currency = serializers.CharField(max_length=3)
    discount = serializers.FloatField(required=False, default=0.0)
    discount_type = serializers.CharField(max_length=10, required= False, allow_blank=True)
    taxable = serializers.BooleanField(required=False, default=0.0)
    total_after_discount = serializers.FloatField(required=False, default=0.0)

class AddressSerializer(serializers.Serializer):
    country = serializers.CharField(max_length=2)
    city = serializers.CharField(max_length=100)
    state = serializers.CharField(max_length=100)
    street = serializers.CharField(max_length=200)
    postal_code = serializers.CharField(max_length=10)

class TransactionSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    type = serializers.CharField(max_length=10)
    line_items = LineItemSerializer(many=True)
    address = AddressSerializer()
    total_txn_amount = serializers.FloatField(required=False, default=0.0)
    taxable_amount = serializers.FloatField(required=False, default=0.0)
    tax_rate = serializers.FloatField(required=False, default=0.0)
    tax_amount = serializers.FloatField(required=False, default=0.0)

class TaxLiabilitySerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    tax = serializers.FloatField(required=False, default=0.0)
    

