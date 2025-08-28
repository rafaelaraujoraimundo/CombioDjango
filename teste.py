import pinggy

# Start an HTTP tunnel forwarding traffic to localhost on port 8080
tunnel = pinggy.start_tunnel(forwardto="179.191.91.6:810", token="P3be4EMjuUl")
print(tunnel)
print(f"Tunnel started with token: {tunnel.token}")