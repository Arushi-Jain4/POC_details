import boto3

#Create S3 bucket
client = boto3.client('s3')
client.create_bucket(
    Bucket='poc-analytics1234',
    CreateBucketConfiguration={
        'LocationConstraint': 'us-east-2'
    }
)
#Upload file in S3 bucket
client.upload_file('C:/Users/arush/Desktop/python-aws/AWS_upload_data.xlsx', 'poc-analytics1234', 'AWS_upload_data.xlsx')

#Create database for Glue
client=boto3.client('glue')
response = client.create_database(
    DatabaseInput={
        'Name': 'POC_DB'
        }
)
#Create crawler
client.create_crawler(
    Name='POC_crawler1',
    Role='service-role/AWSGlueServiceRole-arushi',
    DatabaseName='POC_DB',
    Targets={
        'S3Targets': [
            {
                'Path': 's3://poc-analytics12',
            },
        ],
    }

)
#Run crawler
response = client.start_crawler(
    Name='POC_crawler1'
)

if response is 200:
    #Create Glue Job
    client.create_job(
        Name='POC_Job',
        Role='service-role/AWSGlueServiceRole-arushi',
        Command={
            'Name': 'glueetl',
            'ScriptLocation': 's3://poc-analytics12',
             }
    )
    #Job run
    client.start_job_run(
        JobName='POC_Job',
    )
    



