# Proxy Guide

This guide provides detailed information about setting up and managing proxies for EarnApp RebornX.

## Understanding Proxies

### What is a Proxy?

A proxy server acts as an intermediary between your device and the internet. When you use a proxy, your requests are routed through the proxy server, which then forwards them to the destination website. The website sees the proxy's IP address instead of your actual IP address.

### Why Use Proxies with EarnApp?

EarnApp RebornX allows you to run multiple instances of EarnApp, each with a different IP address. This is achieved by using different proxies for each instance. By using multiple IP addresses, you can potentially increase your earnings.

### Types of Proxies

EarnApp RebornX supports the following types of proxies:

- **HTTP Proxies**: The most common type of proxy. They work with HTTP and HTTPS traffic.
- **SOCKS5 Proxies**: More versatile than HTTP proxies, they can handle any type of traffic, not just HTTP/HTTPS.

## Setting Up Proxies

### Creating the Proxies File

1. Create a file named `proxies.txt` in the root directory of EarnApp RebornX
2. Add your proxies to the file, one per line, using the following format:
   ```
   # Format: protocol://username:password@host:port
   http://user1:pass1@proxy1.example.com:8080
   http://user2:pass2@proxy2.example.com:8080
   ```

### Proxy Format

The proxy format is as follows:

```
protocol://username:password@host:port
```

Where:
- `protocol`: The proxy protocol (http or socks5)
- `username`: Your proxy username (if required)
- `password`: Your proxy password (if required)
- `host`: The proxy server hostname or IP address
- `port`: The proxy server port

### Example Proxies

Here are some example proxies:

```
# HTTP proxies with authentication
http://user1:pass1@proxy1.example.com:8080
http://user2:pass2@proxy2.example.com:8080

# HTTP proxies without authentication
http://proxy3.example.com:8080
http://proxy4.example.com:8080

# SOCKS5 proxies with authentication
socks5://user1:pass1@proxy1.example.com:1080
socks5://user2:pass2@proxy2.example.com:1080

# SOCKS5 proxies without authentication
socks5://proxy3.example.com:1080
socks5://proxy4.example.com:1080
```

## Proxy Providers

### Recommended Proxy Providers

Here are some recommended proxy providers:

- **Bright Data (formerly Luminati)**: Offers a wide range of proxy types and locations
- **Oxylabs**: Provides residential, datacenter, and mobile proxies
- **IPRoyal**: Offers residential and datacenter proxies at competitive prices
- **SmartProxy**: Provides residential, datacenter, and mobile proxies
- **ProxyMesh**: Offers residential and datacenter proxies

### Choosing the Right Proxy

When choosing a proxy provider, consider the following factors:

- **Type**: Residential proxies are generally better for EarnApp than datacenter proxies
- **Location**: Choose proxies from locations with high demand for bandwidth
- **Speed**: Faster proxies will generally result in higher earnings
- **Reliability**: Look for providers with high uptime and good customer support
- **Price**: Compare prices and features to find the best value

### Free vs. Paid Proxies

While it's possible to use free proxies, we strongly recommend using paid proxies for the following reasons:

- **Reliability**: Paid proxies are generally more reliable and have higher uptime
- **Speed**: Paid proxies typically offer better speed and performance
- **Security**: Paid proxies are less likely to be compromised or used for malicious purposes
- **Support**: Paid proxy providers offer customer support to help with issues
- **Earnings**: Better proxies generally result in higher earnings

## Testing Proxies

### Testing Proxy Connectivity

Before using a proxy with EarnApp RebornX, it's a good idea to test its connectivity:

```bash
curl -x http://username:password@host:port https://api.ipify.org
```

If the proxy is working correctly, you should see an IP address that is different from your actual IP address.

### Testing Proxy Speed

To test the speed of a proxy:

```bash
curl -x http://username:password@host:port -o /dev/null -s -w "%{time_total}\n" https://earnapp.com
```

This command will measure the time it takes to connect to earnapp.com through the proxy. Lower times indicate faster proxies.

### Testing Multiple Proxies

If you have many proxies, you can use a script to test them all:

```python
#!/usr/bin/env python3
import requests
import time

def test_proxy(proxy):
    try:
        start_time = time.time()
        response = requests.get('https://api.ipify.org', proxies={'http': proxy, 'https': proxy}, timeout=10)
        end_time = time.time()
        
        if response.status_code == 200:
            print(f"Proxy: {proxy}")
            print(f"IP: {response.text}")
            print(f"Time: {end_time - start_time:.2f} seconds")
            print("---")
            return True
    except:
        print(f"Proxy: {proxy}")
        print("Failed")
        print("---")
        return False

# Read proxies from file
with open('proxies.txt', 'r') as f:
    proxies = [line.strip() for line in f if line.strip() and not line.startswith('#')]

# Test each proxy
for proxy in proxies:
    test_proxy(proxy)
```

## Managing Proxies

### Rotating Proxies

Some proxy providers offer rotating proxies, which automatically change your IP address at regular intervals. This can be useful for avoiding detection and maximizing earnings.

To use rotating proxies with EarnApp RebornX, simply add the rotating proxy URL to your `proxies.txt` file:

```
http://username:password@rotating.proxy-provider.com:8080
```

### Proxy Scheduling

EarnApp RebornX allows you to schedule proxy rotation. To do this, create a file named `proxy_schedule.json` in the root directory:

```json
{
  "schedule": [
    {
      "time": "00:00",
      "proxy": "http://user1:pass1@proxy1.example.com:8080"
    },
    {
      "time": "06:00",
      "proxy": "http://user2:pass2@proxy2.example.com:8080"
    },
    {
      "time": "12:00",
      "proxy": "http://user3:pass3@proxy3.example.com:8080"
    },
    {
      "time": "18:00",
      "proxy": "http://user4:pass4@proxy4.example.com:8080"
    }
  ]
}
```

This will automatically rotate your proxies at the specified times.

### Proxy Health Monitoring

EarnApp RebornX includes a feature to monitor the health of your proxies. To enable this, add the following to your `.env` file:

```
PROXY_HEALTH_CHECK=true
PROXY_HEALTH_CHECK_INTERVAL=300
```

This will check the health of your proxies every 5 minutes (300 seconds) and restart instances using unhealthy proxies.

## Troubleshooting Proxy Issues

### Common Proxy Problems

#### Connection Refused

If you see "Connection refused" errors:

1. Check if the proxy server is online
2. Verify the proxy credentials
3. Check if the proxy port is correct
4. Try a different proxy

#### Slow Connections

If your connections are slow:

1. Try a different proxy provider
2. Choose proxies closer to your location
3. Upgrade to a higher-tier proxy plan
4. Check your internet connection

#### Authentication Errors

If you see authentication errors:

1. Verify your proxy username and password
2. Check if the proxy requires authentication
3. Try a different proxy

### Proxy Logs

To view proxy logs:

```bash
docker logs yourDeviceName_tun2socks
```

This will show you detailed information about the proxy connection, including any errors.

## Advanced Proxy Configuration

### Custom Proxy Settings

You can customize proxy settings by modifying the `docker-compose.yml` file:

```yaml
proxy:
  container_name: ${DEVICE_NAME}_tun2socks
  hostname: ${DEVICE_NAME}_tun2socks
  image: xjasonlyu/tun2socks
  environment:
    - LOGLEVEL=info
    - PROXY=${STACK_PROXY_URL}
    - EXTRA_COMMANDS=ip rule add iif lo ipproto udp dport 53 lookup main;
  cap_add:
    - NET_ADMIN
  privileged: true
  network_mode: bridge
  dns:
    - 1.1.1.1
    - 8.8.8.8
    - 1.0.0.1
    - 8.8.4.4
  ports: []
  volumes:
    - /dev/net/tun:/dev/net/tun
  restart: always
```

### DNS Configuration

You can customize the DNS servers used by the proxy by modifying the `dns` section in the `docker-compose.yml` file:

```yaml
dns:
  - 1.1.1.1
  - 8.8.8.8
  - 1.0.0.1
  - 8.8.4.4
```

### Proxy Timeout Settings

You can adjust the proxy timeout settings by adding the following to the `environment` section in the `docker-compose.yml` file:

```yaml
environment:
  - LOGLEVEL=info
  - PROXY=${STACK_PROXY_URL}
  - EXTRA_COMMANDS=ip rule add iif lo ipproto udp dport 53 lookup main;
  - PROXY_TIMEOUT=30
```

This will set the proxy timeout to 30 seconds.

## Best Practices

### Proxy Selection

- Use residential proxies for better earnings
- Choose proxies from locations with high demand for bandwidth
- Use different proxies for different instances
- Regularly test and replace underperforming proxies

### Security

- Use secure proxies (HTTPS/SOCKS5)
- Regularly rotate proxy credentials
- Monitor proxy health and performance
- Use proxies from reputable providers

### Performance

- Test proxies before using them
- Monitor proxy performance and replace slow proxies
- Use proxies with low latency
- Distribute instances across different proxy providers

### Cost Optimization

- Compare prices and features from different providers
- Start with a small number of proxies and scale up as needed
- Monitor the return on investment for each proxy
- Consider using rotating proxies for cost savings 