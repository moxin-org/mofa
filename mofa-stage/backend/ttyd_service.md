# ttyd Service Integration Guide

This document provides instructions for integrating [ttyd](https://github.com/tsl0922/ttyd) with MoFA_Stage's backend to enable browser-based terminal access without requiring SSH.

## What is ttyd?

ttyd is a simple command-line tool that turns your terminal program into a web application. It allows you to share your terminal session over the web, which is useful for remote access and collaboration.

## Installation

### Ubuntu/Debian

```bash
# Install required dependencies
sudo apt-get update
sudo apt-get install -y build-essential cmake git libjson-c-dev libwebsockets-dev

# Clone ttyd repository
git clone https://github.com/tsl0922/ttyd.git
cd ttyd

# Build ttyd
mkdir build
cd build
cmake ..
make
sudo make install
```

### macOS

```bash
brew install ttyd
```

### Verification

After installation, verify that ttyd is installed correctly:

```bash
ttyd --version
```

## Running ttyd as a Service

### 1. Create a systemd service file

Create a new file `/etc/systemd/system/ttyd.service`:

```bash
sudo nano /etc/systemd/system/ttyd.service
```

Add the following content:

```ini
[Unit]
Description=TTY Daemon Service
After=network.target

[Service]
ExecStart=/usr/local/bin/ttyd -p 7681 -i localhost bash
Restart=always
WorkingDirectory=/home/username
User=username
Group=username
Environment="PATH=/usr/local/bin:/usr/bin:/bin"

[Install]
WantedBy=multi-user.target
```

Replace `username` with your actual username. Adjust the `WorkingDirectory` as needed.

### 2. Start and enable the service

```bash
sudo systemctl daemon-reload
sudo systemctl start ttyd
sudo systemctl enable ttyd
```

### 3. Check the service status

```bash
sudo systemctl status ttyd
```

## Configuration Options

For the MoFA_Stage integration, we recommend the following configuration:

```bash
ttyd -p 7681 -i localhost -m 1 -t fontFamily="'Courier New',monospace" -t fontSize=14 bash
```

This:
- Binds to port 7681
- Only listens on localhost for security
- Limits max clients to 1 per browser session
- Sets font family and size
- Uses bash as the shell

## Security Considerations

1. **Network Access**: By default, ttyd binds to all interfaces. Use `-i localhost` to restrict access to local connections only.

2. **Reverse Proxy**: Configure a reverse proxy (nginx/Apache) to handle SSL and provide additional security.

3. **Authentication**: Use the `-c username:password` option to enable basic authentication.

## Integration with MoFA_Stage

### Reverse Proxy Configuration (Nginx)

```
location /ttyd/ {
    proxy_pass http://localhost:7681/;
    proxy_http_version 1.1;
    proxy_set_header Upgrade $http_upgrade;
    proxy_set_header Connection "upgrade";
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
}
```

### Multiple Terminal Instances

To support multiple terminal instances with different working directories or commands, you could create separate ttyd instances on different ports:

```bash
# Default terminal
ttyd -p 7681 -i localhost bash

# Terminal in MoFA directory  
ttyd -p 7682 -i localhost -c "/path/to/mofa_dir" bash
```

Then update the frontend to point to the correct port for each tab.

## Troubleshooting

1. **Port already in use**: Check if another process is using port 7681:
   ```bash
   sudo lsof -i :7681
   ```

2. **Connection refused**: Ensure ttyd is running and listening on the correct interface:
   ```bash
   ps aux | grep ttyd
   netstat -tulpn | grep 7681
   ```

3. **Cross-Origin issues**: If the frontend is on a different domain/port than ttyd, you might need to enable CORS.

## Resources

- [ttyd GitHub repository](https://github.com/tsl0922/ttyd)
- [ttyd documentation](https://github.com/tsl0922/ttyd/blob/main/README.md) 