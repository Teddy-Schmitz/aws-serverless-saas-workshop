import json
import os
import stripe
import boto3
import logger
import utils

region = os.environ['AWS_REGION']
secret_key = os.environ['STRIPE_SECRET_KEY_ARN']

lambda_client = boto3.client('lambda')
secrets = boto3.client('secretsmanager')

def tenant_subscription(event, context):
    id = event['pathParameters']['id']
    res = secrets.get_secret_value(SecretId=secret_key)
    stripe.api_key = res['SecretString']
    try:
        checkout = stripe.checkout.Session.retrieve(id)
        sub = stripe.Subscription.retrieve(checkout.subscription, expand=['items.data.price.product'])
        checkout['product'] = sub['items']['data'][0]['price']['product']
        response_json = checkout
    except Exception as e :
        logger.error('Error retrieving subscription information')
        raise Exception('Error retrieving subscription information', e) 
    else:
        return utils.create_success_response(response_json)
