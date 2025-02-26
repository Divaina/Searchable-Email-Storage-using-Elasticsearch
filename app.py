import asyncio
import imaplib
import email
from email.header import decode_header
from elasticsearch import Elasticsearch, helpers

# === Configuration ===
EMAIL_ACCOUNT = "your_email@gmail.com"
EMAIL_PASSWORD = "your_app_password"  # Use an App Password
IMAP_SERVER = "imap.gmail.com"  # Change for Outlook/Yahoo

# Connect to Elasticsearch
es = Elasticsearch("http://localhost:9200")
INDEX_NAME = "emails"

# === Step 1: Create Elasticsearch Index (if not exists) ===
def create_index():
    """Creates an Elasticsearch index with optimized mappings."""
    email_index = {
        "settings": {"number_of_shards": 1, "number_of_replicas": 0},
        "mappings": {
            "properties": {
                "subject": {"type": "text"},
                "sender": {"type": "keyword"},
                "date": {"type": "date"},
                "content": {"type": "text"},
                "folder": {"type": "keyword"},
                "account": {"type": "keyword"}
            }
        }
    }
    if not es.indices.exists(index=INDEX_NAME):
        es.indices.create(index=INDEX_NAME, body=email_index)
        print(f"Index '{INDEX_NAME}' created successfully!")

# === Step 2: Fetch and Process Emails (Async) ===
async def fetch_emails():
    """Fetches emails from IMAP and indexes them in Elasticsearch in bulk."""
    try:
        mail = imaplib.IMAP4_SSL(IMAP_SERVER)
        mail.login(EMAIL_ACCOUNT, EMAIL_PASSWORD)
        mail.select("INBOX")

        status, email_ids = mail.search(None, "ALL")
        email_ids = email_ids[0].split()

        emails = []  # Store emails for bulk indexing
        for e_id in email_ids[:20]:  # Fetch limited emails for optimization
            _, msg_data = mail.fetch(e_id, "(RFC822)")
            for response_part in msg_data:
                if isinstance(response_part, tuple):
                    msg = email.message_from_bytes(response_part[1])
                    subject, encoding = decode_header(msg["Subject"])[0]
                    sender = msg.get("From")
                    date = msg.get("Date")

                    if isinstance(subject, bytes):
                        subject = subject.decode(encoding or "utf-8")

                    content = ""
                    if msg.is_multipart():
                        for part in msg.walk():
                            if part.get_content_type() == "text/plain":
                                content = part.get_payload(decode=True).decode(errors="ignore")
                                break
                    else:
                        content = msg.get_payload(decode=True).decode(errors="ignore")

                    emails.append({
                        "_index": INDEX_NAME,
                        "_source": {
                            "subject": subject,
                            "sender": sender,
                            "date": date,
                            "content": content,
                            "folder": "INBOX",
                            "account": EMAIL_ACCOUNT
                        }
                    })

        mail.logout()

        if emails:
            helpers.bulk(es, emails)
            print(f" Indexed {len(emails)} emails successfully!")

    except Exception as e:
        print(f" Error fetching emails: {e}")

# === Step 3: Search Emails ===
def search_emails(query, size=5):
    """Performs a full-text search in Elasticsearch."""
    search_query = {
        "size": size,
        "query": {"multi_match": {"query": query, "fields": ["subject", "content"]}}
    }
    results = es.search(index=INDEX_NAME, body=search_query)

    return [
        {"subject": hit["_source"]["subject"], "sender": hit["_source"]["sender"]}
        for hit in results["hits"]["hits"]
    ]

# === Step 4: Filter Emails by Folder & Account ===
def filter_by_folder_account(folder, account, size=5):
    """Filters emails by folder and account."""
    filter_query = {
        "size": size,
        "query": {
            "bool": {
                "must": [{"term": {"folder": folder}}, {"term": {"account": account}}]
            }
        }
    }
    results = es.search(index=INDEX_NAME, body=filter_query)

    return [
        {"subject": hit["_source"]["subject"], "sender": hit["_source"]["sender"]}
        for hit in results["hits"]["hits"]
    ]

# === Run the Setup ===
if __name__ == "__main__":
    create_index()  # Create Elasticsearch Index
    
    # Run email fetching asynchronously
    asyncio.run(fetch_emails())

    # Example Queries
    print("\n Search results for 'meeting':")
    for email in search_emails("meeting"):
        print(f" {email['subject']} - {email['sender']}")

    print("\n Filtering emails in INBOX for your email:")
    for email in filter_by_folder_account("INBOX", EMAIL_ACCOUNT):
        print(f" {email['subject']} - {email['sender']}")

