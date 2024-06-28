import os
from dotenv import load_dotenv

load_dotenv()


from django.core.management.base import BaseCommand
from sqlalchemy.orm import Session
from sqlalchemy_config import get_db
from sphere_backend.models import Transaction, LineItem, Address, TaxLiability
from sphere_backend.serializers import TransactionSerializer
import requests

class Command(BaseCommand):
    help = 'Processes transactions from sphere API and stores them in the database.'

    def handle(self, *args, **kwargs):
        db: Session = next(get_db())
        api_url = os.getenv('API_URL') 
        
        headers = {
            'Authorization': f'Bearer {os.getenv("API_TOKEN")}',
            'Content-Type': 'application/json'
        }

        try:

            db.query(LineItem).delete()
            db.query(Address).delete()
            db.query(Transaction).delete()
            db.query(TaxLiability).delete()

            db.commit()


            response = requests.get(api_url,headers=headers)
            response.raise_for_status()

            transactions_data = response.json()["transactions"]
            tax_authority_data = response.json()["tax_authority"]

            
            tax_details = {}
            for item in tax_authority_data:
                tax_details[item["name"]] = {
                    "rate" : item["rate"],
                    "taxable_items" : set(item["taxable_items"])
                }
            
            # print(tax_details)

            tax_liability = 0
            txn_counter = 0


            for transaction_data in transactions_data:
                txn_counter += 1
                serializer = TransactionSerializer(data=transaction_data)
                if serializer.is_valid():
                    address_data = serializer.validated_data['address']
                    
                    tax_key = address_data['state']+"_"+address_data['country']
                    tax_key = tax_key.lower()

                    new_transaction = Transaction(
                        type=serializer.validated_data['type'],
                        tax_rate = float(tax_details[tax_key]['rate'])
                        )
                    db.add(new_transaction)
                    db.commit()
                    db.refresh(new_transaction)

                    total_txn_amount = 0.0
                    txn_tax_amount = 0.0
                    taxable_amount = 0.0

                    for item_data in serializer.validated_data['line_items']:

                        new_item = LineItem(
                            transaction_id=new_transaction.id,
                            name=item_data['name'],
                            price=item_data['price'],
                            quantity=item_data['quantity'],
                            currency=item_data['currency'],
                            discount=item_data.get('discount', 0.0),
                            discount_type=item_data.get('discount_type', ""),
                            taxable = True if item_data["name"] in tax_details[tax_key]['taxable_items'] else False
                        )
                        db.add(new_item)
                        total_after_discount = self.get_effective_price(new_item.price, new_item.quantity, new_item.discount, new_item.discount_type)

                        new_item.total_after_discount = total_after_discount

                        if new_item.taxable == True:
                            taxable_amount += new_item.total_after_discount
                        total_txn_amount += new_item.total_after_discount
                    
                        
                    
                    txn_tax_amount += self.calculate_tax(taxable_amount, new_transaction.tax_rate, new_transaction.type)
                    new_transaction.tax_amount = txn_tax_amount
                    new_transaction.taxable_amount = taxable_amount
                    new_transaction.total_txn_amount = total_txn_amount

                    address_data = serializer.validated_data['address']
                    new_address = Address(
                        transaction_id=new_transaction.id,
                        country=address_data['country'],
                        city=address_data['city'],
                        state=address_data['state'],
                        street=address_data['street'],
                        postal_code=address_data['postal_code']
                        
                    )
                    db.add(new_address)
                    db.commit()
                    tax_liability += txn_tax_amount

            tax_liability = round(tax_liability,2)
            db.add(TaxLiability(tax=tax_liability))
            db.commit()
            self.stdout.write(self.style.SUCCESS('Successfully fetched and stored transactions.'))
            self.stdout.write(self.style.SUCCESS(f'Total transactions processed: {txn_counter}'))
            self.stdout.write(self.style.SUCCESS(f'Total Liability:{tax_liability}'))

        except requests.exceptions.RequestException as e:
            self.stdout.write(self.style.ERROR(f'Failed to fetch transactions: {str(e)}'))
        
    def get_effective_price(self, price, qty, discount, discount_type):
        price = price*qty
        if discount_type == "":
            return price
        elif discount_type == "amount":
            return price - discount
        elif discount_type == "percentage":
            return price - (price*(discount/100))
        else:
            return price

    def calculate_tax(self, price, tax_rate, txn_type):
        tax = price * (tax_rate/100)
        
        if txn_type == "debit":
            tax = -1.0 * tax

        tax = round(tax,2)
        return tax