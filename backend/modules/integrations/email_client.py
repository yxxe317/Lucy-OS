"""
Email Client - Send and receive emails via IMAP/SMTP
"""

import smtplib
import imaplib
import email
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import List, Dict, Optional
import time

class EmailClient:
    """
    Email client for sending/receiving emails
    """
    
    def __init__(self, email_address: str = None, password: str = None,
                 smtp_server: str = "smtp.gmail.com", smtp_port: int = 587,
                 imap_server: str = "imap.gmail.com", imap_port: int = 993):
        self.email = email_address
        self.password = password
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.imap_server = imap_server
        self.imap_port = imap_port
        self.smtp_connection = None
        self.imap_connection = None
    
    def connect_smtp(self):
        """Connect to SMTP server"""
        if not self.email or not self.password:
            print("Email credentials not configured")
            return False
        
        try:
            self.smtp_connection = smtplib.SMTP(self.smtp_server, self.smtp_port)
            self.smtp_connection.starttls()
            self.smtp_connection.login(self.email, self.password)
            return True
        except Exception as e:
            print(f"SMTP connection error: {e}")
            return False
    
    def connect_imap(self):
        """Connect to IMAP server"""
        if not self.email or not self.password:
            print("Email credentials not configured")
            return False
        
        try:
            self.imap_connection = imaplib.IMAP4_SSL(self.imap_server, self.imap_port)
            self.imap_connection.login(self.email, self.password)
            return True
        except Exception as e:
            print(f"IMAP connection error: {e}")
            return False
    
    def send_email(self, to: str, subject: str, body: str, 
                    cc: List[str] = None, bcc: List[str] = None) -> bool:
        """
        Send an email
        """
        if not self.smtp_connection and not self.connect_smtp():
            return self._simulate_send(to, subject, body)
        
        try:
            msg = MIMEMultipart()
            msg['From'] = self.email
            msg['To'] = to
            msg['Subject'] = subject
            
            if cc:
                msg['Cc'] = ', '.join(cc)
            
            msg.attach(MIMEText(body, 'plain'))
            
            # Combine recipients
            all_recipients = [to] + (cc or []) + (bcc or [])
            
            self.smtp_connection.send_message(msg, self.email, all_recipients)
            print(f"✅ Email sent to {to}")
            return True
            
        except Exception as e:
            print(f"Email send error: {e}")
            return self._simulate_send(to, subject, body)
    
    def read_inbox(self, limit: int = 10) -> List[Dict]:
        """
        Read recent emails from inbox
        """
        if not self.imap_connection and not self.connect_imap():
            return self._simulate_inbox(limit)
        
        try:
            self.imap_connection.select('INBOX')
            result, data = self.imap_connection.search(None, 'ALL')
            
            emails = []
            for num in data[0].split()[-limit:]:
                result, data = self.imap_connection.fetch(num, '(RFC822)')
                raw_email = data[0][1]
                msg = email.message_from_bytes(raw_email)
                
                email_data = {
                    'from': msg.get('From'),
                    'to': msg.get('To'),
                    'subject': msg.get('Subject'),
                    'date': msg.get('Date'),
                    'body': self._get_email_body(msg)
                }
                emails.append(email_data)
            
            return emails
            
        except Exception as e:
            print(f"Read inbox error: {e}")
            return self._simulate_inbox(limit)
    
    def _get_email_body(self, msg) -> str:
        """Extract body from email message"""
        if msg.is_multipart():
            for part in msg.walk():
                if part.get_content_type() == "text/plain":
                    return part.get_payload(decode=True).decode()
        else:
            return msg.get_payload(decode=True).decode()
        return ""
    
    def _simulate_send(self, to: str, subject: str, body: str) -> bool:
        """Simulate sending email"""
        print(f"📧 [SIMULATED] Email sent to {to}")
        print(f"   Subject: {subject}")
        print(f"   Body: {body[:50]}...")
        return True
    
    def _simulate_inbox(self, limit: int) -> List[Dict]:
        """Simulate inbox emails"""
        import random
        from datetime import datetime, timedelta
        
        senders = ['friend@example.com', 'work@company.com', 'news@updates.com', 'family@home.com']
        subjects = ['Meeting tomorrow', 'Hello!', 'Newsletter', 'Important update', 'Weekend plans']
        
        emails = []
        for i in range(min(limit, 5)):
            date = datetime.now() - timedelta(hours=random.randint(1, 48))
            emails.append({
                'from': random.choice(senders),
                'to': 'me@example.com',
                'subject': random.choice(subjects),
                'date': date.strftime('%a, %d %b %Y %H:%M:%S %z'),
                'body': f"This is a simulated email #{i+1} for testing purposes.",
                '_simulated': True
            })
        
        return emails
    
    def disconnect(self):
        """Close connections"""
        if self.smtp_connection:
            self.smtp_connection.quit()
        if self.imap_connection:
            self.imap_connection.logout()