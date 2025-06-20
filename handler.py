import json
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

load_dotenv()

def send_email(event, context):
    try:

        body = json.loads(event.get('body', '{}'))
        

        required_fields = ['receiver_email', 'subject', 'body_text']
        for field in required_fields:
            if field not in body:
                return {
                    'statusCode': 400,
                    'body': json.dumps({'error': f'Missing required field: {field}'})
                }
        

        email_provider = os.environ.get('EMAIL_PROVIDER', 'smtp.gmail.com')
        email_username = os.environ.get('SENDER_EMAIL')
        email_password = os.environ.get('SENDER_PASSWORD')
        
        if not email_username or not email_password:
            return {
                'statusCode': 500,
                'body': json.dumps({'error': 'Email server credentials not configured'})
            }
        

        msg = MIMEMultipart()
        msg['From'] = email_username
        msg['To'] = body['receiver_email']
        msg['Subject'] = body['subject']
        

        msg.attach(MIMEText(body['body_text'], 'plain'))
        

        with smtplib.SMTP(email_provider, 587) as server:
            server.starttls()
            server.login(email_username, email_password)
            server.send_message(msg)
        
        # Return success response
        return {
            'statusCode': 200,
            'body': json.dumps({'message': 'Email sent successfully'})
        }
    
    except json.JSONDecodeError:
        return {
            'statusCode': 400,
            'body': json.dumps({'error': 'Invalid JSON format'})
        }
    except smtplib.SMTPException as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': f'Failed to send email: {str(e)}'})
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': f'Unexpected error: {str(e)}'})
        }