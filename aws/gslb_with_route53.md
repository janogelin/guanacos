# GSLB with AWS Route 53

## Overview

Use **Global Server Load Balancing (GSLB)** with **Route 53** to direct global traffic to the nearest healthy region and failover to a secondary region when needed.

---

## Architecture

### Components:
- **Route 53** for DNS and global routing
- **Latency-based routing** or **Geo DNS**
- **Health checks** for automatic failover
- **Regional deployments** (e.g., `us-east-1`, `eu-west-1`)

---

## Step-by-Step Guide

### 1. Deploy Workloads in Multiple Regions

Example:
- `us-east-1`: `llm.useast.yourdomain.com`
- `eu-west-1`: `llm.euwest.yourdomain.com`

---

### 2. Create a Route 53 Hosted Zone

Create a hosted zone for `yourdomain.com`.

---

### 3. Add Latency-based Routing Records

#### Record for US East:

| Field             | Value                          |
|------------------|--------------------------------|
| Name              | `llm.yourdomain.com`          |
| Type              | A or CNAME                    |
| Alias/Target      | ALB or IP in `us-east-1`      |
| Routing Policy    | Latency                       |
| Region            | `us-east-1`                   |
| Health Check      | `us-east-health-check`        |

#### Record for EU West:

Same fields, target `eu-west-1`.

---

### 4. Set Up Health Checks

- Type: HTTP/HTTPS
- Endpoint: `/healthz` on each region’s load balancer
- Purpose: Automatic failover if a region is unavailable

---

### 5. Test Routing

Run:

```bash
dig +short llm.yourdomain.com
```

From different geographic locations to verify region-specific IPs.

---

## Optional Enhancements

### Geo DNS:
Force users from specific geos to use specific regions.

### Failover Routing:
Designate a primary region and a backup region.

---

## Third-party GSLB Alternatives

For advanced control and visibility:
- **NS1**
- **Akamai GTM**
- **F5 GTM**
- **Cloudflare Load Balancing**

---

## Best Practices

- Use short TTLs (30–60s) for responsiveness
- Monitor health check metrics
- Use HTTPS and proper TLS configuration
- Combine with CDN for latency-sensitive apps

---

## Summary

Route 53 provides a simple but powerful GSLB mechanism using native AWS services. Combine latency routing and health checks to ensure global availability and low latency.
