# 🪣 Amazon S3 (Simple Storage Service) — Quick Overview

> **Amazon S3** is AWS's object storage service that lets you store and retrieve any amount of data from anywhere on the internet.

---

## 📌 What is S3?

- S3 stores data as **objects** (files) inside **buckets** (containers)
- Each object can be up to **5 TB** in size
- Buckets are globally unique and tied to a specific AWS region
- Offers **11 nines of durability** (99.999999999%) — your data is extremely safe

---

## 🧱 Core Concepts

| Concept | Description |
|---------|-------------|
| **Bucket** | A container that holds your objects (like a folder) |
| **Object** | A file stored in a bucket (data + metadata + key) |
| **Key** | The unique name/path of an object inside a bucket |
| **Region** | The AWS location where your bucket is stored |

---

## 🗂️ Storage Classes

S3 offers different storage tiers based on how often you access your data:

| Storage Class | Best For | Cost |
|---------------|----------|------|
| **S3 Standard** | Frequently accessed data | $$$ |
| **S3 Intelligent-Tiering** | Unknown access patterns | $$ |
| **S3 Standard-IA** | Infrequent access | $$ |
| **S3 Glacier** | Long-term archival | ¢ |
| **S3 Glacier Deep Archive** | Rarely accessed, 7–10yr archive | ¢¢ |

---

## ⚙️ Key Features

- 🔒 **Security** — Bucket policies, IAM roles, ACLs, and SSE encryption
- 🌍 **Static Website Hosting** — Host a website directly from an S3 bucket
- 📦 **Versioning** — Keep multiple versions of an object
- 🔁 **Lifecycle Policies** — Auto-move or delete objects after a set time
- 🌐 **Cross-Region Replication (CRR)** — Replicate data across AWS regions
- ⚡ **S3 Transfer Acceleration** — Speed up uploads using AWS edge locations

---

## 🚀 Common Use Cases

1. **Backup & Restore** — Store database snapshots and system backups
2. **Static Website Hosting** — Serve HTML, CSS, JS files directly
3. **Data Lake** — Central storage for analytics and big data pipelines
4. **Media Storage** — Store images, videos, and audio files
5. **Application Assets** — Store user uploads, logs, and config files
6. **ML Training Data** — Feed datasets into SageMaker or Bedrock

---

## 🛠️ Basic AWS CLI Commands

```bash
# Create a bucket
aws s3 mb s3://my-bucket-name

# Upload a file
aws s3 cp myfile.txt s3://my-bucket-name/

# List objects in a bucket
aws s3 ls s3://my-bucket-name/

# Download a file
aws s3 cp s3://my-bucket-name/myfile.txt ./myfile.txt

# Delete a file
aws s3 rm s3://my-bucket-name/myfile.txt

# Sync a local folder to S3
aws s3 sync ./my-folder s3://my-bucket-name/my-folder
```

---

## 💰 Pricing (Summary)

- **Storage**: ~$0.023 per GB/month (S3 Standard, us-east-1)
- **Requests**: ~$0.0004 per 1,000 GET requests
- **Data Transfer OUT**: First 100 GB/month free, then ~$0.09/GB
- **Free Tier**: 5 GB storage + 20,000 GET + 2,000 PUT requests/month (12 months)

---

## 🔐 Quick Security Tips

1. ✅ **Block all public access** unless explicitly needed
2. ✅ **Enable versioning** to protect against accidental deletes
3. ✅ **Use bucket policies** to restrict access by IAM role or IP
4. ✅ **Enable server-side encryption (SSE-S3 or SSE-KMS)**
5. ✅ **Enable access logging** to track who accesses your data

---

> 📎 **Official Docs**: [docs.aws.amazon.com/s3](https://docs.aws.amazon.com/s3/index.html)
> 💰 **Pricing**: [aws.amazon.com/s3/pricing](https://aws.amazon.com/s3/pricing/)

---

*S3 Mini Guide — Part of AI Summit Labs / Lab 01*
