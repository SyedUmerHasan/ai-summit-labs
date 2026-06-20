# 🔱 Amazon Neptune DB — Complete Guide

> **Amazon Neptune** is a fully managed graph database service by AWS, designed for highly connected datasets. It supports both **Property Graph** and **RDF** models.

---

## 📌 Table of Contents

- [Overview](#overview)
- [Key Features](#key-features)
- [Supported Query Languages](#supported-query-languages)
- [Architecture](#architecture)
- [Getting Started](#getting-started)
- [Gremlin Query Examples](#gremlin-query-examples)
- [SPARQL Query Examples](#sparql-query-examples)
- [Security & Networking](#security--networking)
- [Pricing Highlights](#pricing-highlights)
- [Best Practices](#best-practices)
- [Useful Resources](#useful-resources)

---

## 🌐 Overview

Amazon Neptune is optimized for storing and querying **billions of relationships** with **millisecond latency**. It is ideal for use cases such as:

| Use Case               | Description                                      |
|------------------------|--------------------------------------------------|
| 🧠 Knowledge Graphs     | Build intelligent, connected knowledge bases     |
| 🔍 Fraud Detection      | Detect complex fraud patterns in real-time       |
| 🤝 Social Networks      | Model users, relationships, and interactions     |
| 🧬 Life Sciences        | Analyze biological pathways and gene networks    |
| 🔗 Recommendation Engines | Suggest products/content based on connections |

---

## ✨ Key Features

- ✅ **Fully Managed** — No infrastructure management needed
- ✅ **Highly Available** — Replicates 6 copies of data across 3 Availability Zones
- ✅ **Durable Storage** — Continuously backed up to Amazon S3
- ✅ **Fast Failover** — Automatic failover in under 30 seconds
- ✅ **Scalable** — Read replicas for horizontal scaling
- ✅ **Secure** — VPC isolation, encryption at rest & in transit
- ✅ **Serverless Option** — Neptune Serverless for variable workloads

---

## 🗣️ Supported Query Languages

Neptune supports **two graph models** and their respective query languages:

### 🔷 Property Graph
```
Query Language: Apache TinkerPop Gremlin
Endpoint Port : 8182
Protocol      : WebSocket / HTTP
```

### 🔶 RDF Graph (Resource Description Framework)
```
Query Language: SPARQL 1.1
Endpoint Port : 8182
Protocol      : HTTP
```

### 🆕 openCypher (Preview)
```
Query Language: openCypher
Compatible With: Neo4j migrations
Protocol      : Bolt / HTTP
```

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────┐
│                    Your Application                  │
└────────────────────────┬────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────┐
│              Amazon VPC (Private Subnet)             │
│                                                     │
│   ┌─────────────────────────────────────────────┐   │
│   │          Neptune Cluster Endpoint           │   │
│   │  ┌──────────────┐  ┌─────────────────────┐  │   │
│   │  │ Primary (R/W)│  │ Read Replicas (R/O) │  │   │
│   │  └──────────────┘  └─────────────────────┘  │   │
│   └─────────────────────────────────────────────┘   │
│                         │                           │
│   ┌─────────────────────▼───────────────────────┐   │
│   │        Neptune Storage Layer (SSD)          │   │
│   │     6 Copies across 3 Availability Zones    │   │
│   └─────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────┘
                         │
                         ▼
              ┌──────────────────┐
              │   Amazon S3      │
              │ (Continuous Backup)│
              └──────────────────┘
```

---

## 🚀 Getting Started

### Step 1 — Create a Neptune Cluster (AWS CLI)

```bash
aws neptune create-db-cluster \
  --db-cluster-identifier my-neptune-cluster \
  --engine neptune \
  --vpc-security-group-ids sg-xxxxxxxx \
  --db-subnet-group-name my-subnet-group \
  --availability-zones us-east-1a us-east-1b us-east-1c
```

### Step 2 — Create a DB Instance

```bash
aws neptune create-db-instance \
  --db-instance-identifier my-neptune-instance \
  --db-cluster-identifier my-neptune-cluster \
  --engine neptune \
  --db-instance-class db.r5.large
```

### Step 3 — Connect to Neptune

```bash
# Gremlin Console Connection
:remote connect tinkerpop.server conf/neptune-remote.yaml
:remote console

# HTTP Gremlin Endpoint
curl -X POST \
  -H "Content-Type: application/json" \
  "https://<your-neptune-endpoint>:8182/gremlin" \
  -d '{"gremlin": "g.V().limit(5)"}'
```

---

## 🟢 Gremlin Query Examples

### Add Vertices (Nodes)

```groovy
// Add a Person vertex
g.addV('person')
  .property('id', 'p1')
  .property('name', 'Alice')
  .property('age', 30)

// Add another Person vertex
g.addV('person')
  .property('id', 'p2')
  .property('name', 'Bob')
  .property('age', 25)
```

### Add Edges (Relationships)

```groovy
// Alice KNOWS Bob
g.V().has('person', 'name', 'Alice')
  .addE('knows')
  .to(g.V().has('person', 'name', 'Bob'))
  .property('since', 2020)
```

### Traversal Queries

```groovy
// Get all vertices
g.V()

// Get all persons
g.V().hasLabel('person')

// Find who Alice knows
g.V().has('person', 'name', 'Alice').out('knows').values('name')

// Count all edges
g.E().count()

// Find shortest path between two nodes
g.V('p1').repeat(out().simplePath()).until(hasId('p5')).path().limit(1)
```

---

## 🟡 SPARQL Query Examples

### Insert RDF Triple

```sparql
PREFIX ex: <http://example.org/>

INSERT DATA {
  ex:Alice ex:knows ex:Bob .
  ex:Alice ex:age  "30"^^xsd:integer .
  ex:Bob   ex:age  "25"^^xsd:integer .
}
```

### Select Query

```sparql
PREFIX ex: <http://example.org/>

SELECT ?person ?age
WHERE {
  ?person ex:age ?age .
  FILTER(?age > 20)
}
ORDER BY ?age
```

### Ask Query

```sparql
PREFIX ex: <http://example.org/>

ASK {
  ex:Alice ex:knows ex:Bob .
}
```

---

## 🔒 Security & Networking

| Security Feature         | Details                                              |
|--------------------------|------------------------------------------------------|
| 🔐 **VPC Isolation**      | Neptune runs inside your private VPC                 |
| 🔑 **IAM Authentication** | Fine-grained access control via IAM policies         |
| 🔒 **Encryption at Rest** | AES-256 via AWS KMS                                  |
| 🔒 **Encryption in Transit** | TLS 1.2+ enforced                               |
| 🛡️ **Security Groups**    | Control inbound/outbound traffic at instance level   |
| 📋 **Audit Logs**         | CloudWatch Logs integration for query auditing       |

### Sample IAM Policy for Neptune Access

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "neptune-db:connect",
        "neptune-db:ReadDataViaQuery",
        "neptune-db:WriteDataViaQuery"
      ],
      "Resource": "arn:aws:neptune-db:us-east-1:123456789012:cluster-XXXXXXXX/*"
    }
  ]
}
```

---

## 💰 Pricing Highlights

> ⚠️ *Prices vary by region. Always check the [AWS Neptune Pricing Page](https://aws.amazon.com/neptune/pricing/) for the latest.*

| Component             | Details                                         |
|-----------------------|-------------------------------------------------|
| 💻 **Instance Hours**  | Billed per hour based on instance type          |
| 💾 **Storage**         | $0.10 per GB-month                              |
| 📤 **I/O Requests**    | $0.20 per 1 million requests                    |
| 🔄 **Backup Storage**  | Free up to DB size; $0.021/GB-month beyond      |
| 🌍 **Data Transfer**   | Standard AWS data transfer rates apply          |

---

## 💡 Best Practices

1. **🔁 Use Read Replicas** — Distribute read-heavy workloads across replicas
2. **📦 Bulk Load via S3** — Use the Neptune Loader for large dataset ingestion
3. **🗂️ Use Proper Indexing** — Design your graph schema to minimize full scans
4. **📊 Monitor with CloudWatch** — Track `GremlinRequestsPerSec`, `BufferCacheHitRatio`, `CPUUtilization`
5. **🔐 Enable IAM Auth** — Always use IAM-based authentication in production
6. **⚡ Use Neptune Serverless** — For unpredictable or spiky workloads
7. **📁 Enable Audit Logs** — Log all queries for compliance and debugging
8. **🧪 Test Traversals Locally** — Use TinkerPop / Gremlin Server locally before deploying

---

## 📚 Useful Resources

| Resource | Link |
|----------|------|
| 📖 Official Docs | [docs.aws.amazon.com/neptune](https://docs.aws.amazon.com/neptune/latest/userguide/intro.html) |
| 💰 Pricing | [aws.amazon.com/neptune/pricing](https://aws.amazon.com/neptune/pricing/) |
| 🛠️ Gremlin Docs | [tinkerpop.apache.org](https://tinkerpop.apache.org/docs/current/reference/) |
| 🔍 SPARQL W3C Spec | [w3.org/TR/sparql11-query](https://www.w3.org/TR/sparql11-query/) |
| 🧪 Neptune Notebook | [GitHub - aws/graph-notebook](https://github.com/aws/graph-notebook) |
| 🎓 AWS Training | [explore.skillbuilder.aws](https://explore.skillbuilder.aws) |

---

## 🏷️ Tags

`#AWS` `#Neptune` `#GraphDatabase` `#Gremlin` `#SPARQL` `#CloudDatabase` `#NoSQL` `#GraphQL` `#AWSCloud` `#DatabaseEngineering`

---

<div align="center">

**Made with ❤️ for the AI Summit Labs — Lab 01**

*Amazon Neptune DB Reference Guide — v1.0.0*

</div>
