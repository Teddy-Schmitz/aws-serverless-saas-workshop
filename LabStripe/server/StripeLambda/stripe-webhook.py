# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: MIT-0

import boto3
import os
import utils
import stripe
from boto3.dynamodb.conditions import Key

region = os.environ['AWS_REGION']
secret_key = os.environ['STRIPE_SECRET_KEY_ARN']

secrets = boto3.client('secretsmanager')
dynamodb = boto3.resource('dynamodb')
table_tenant_details = dynamodb.Table('ServerlessSaaS-TenantDetails')

lambda_client = boto3.client('lambda')

def update_tenant(event, context):
    stripeEvent = event['detail']

    if stripeEvent['type'] == 'customer.subscription.updated':
        print('update subscription')
        customerID = stripeEvent['data']['object']['customer']
        productID = stripeEvent['data']['object']['plan']['product']

        res = secrets.get_secret_value(SecretId=secret_key)
        stripe.api_key = res['SecretString']

        # Uncomment all the below lines to update dynamodb
        # product = stripe.Product.retrieve(productID)

        # response = table_tenant_details.query(
        #     IndexName="ServerlessSaas-StripeID",
        #     KeyConditionExpression=Key('stripeID').eq(customerID),
        #     ProjectionExpression="tenantId"
        # )
        # print(response)
        # if (response['Count'] == 1):
        #     response_update = table_tenant_details.update_item(
        #         Key={
        #             'tenantId': response['Items'][0]['tenantId'],
        #         },
        #         UpdateExpression="set tenantTier=:tenantTier",
        #         ExpressionAttributeValues={
        #                 ':tenantTier': product.name
        #             },
        #         ReturnValues="UPDATED_NEW"
        #         )             

        # return utils.create_success_response("Tenant Updated")
    else:
        return utils.create_unauthorized_response()
