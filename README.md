# Fast ILO Exporter
A basic prometheus exporter for HP servers with an ILO controller which uses SNMP (and optionally HTTPS) to attempt to strike a balance between frequency and detail of metrics.

## testing
I have tested this on a single server (my dl380p gen8) with ILO4, as I do not own any other servers with an ILO controller.

It works for me, but might not for you.

## Setting up the ILO
HP does not allow reading SNMP by default, so you need to enable it.

### SNMP
1. Log into your ILO dashboard.
2. Go to **Administration > Management**
3. Under **SNMP Settings** set the **Read community** to whatever you want (but remember it for later!)
4. Click **Apply**

### HTTPS (optional)
1. Log into your ILO dashboard.
2. Go to **Administration > User Administration**
3. Add a new user 
   - Set the username and password to whatever you want (also remember this)
   - I recommend not selecting any permissions, as they are not necessary

## Setting up the exporter
These steps are copied from my notes and detail the general process I go through to install any exporter. They were written to run on Debian 12.

### download
Grab the latest release from the [releases tab](https://github.com/Benjamin-Wiegand/ilo_exporter/releases).
Replace `$DOWNLOAD_URL` with the appropriate download url.

```bash
cd ~
curl $DOWNLOAD_URL -Lo ilo_exporter.tar.gz

# extract
tar -xvf ilo_exporter.tar.gz
rm ilo_exporter.tar.gz
```

### install
create a daemon user and prepare the file structure

```bash
# daemon user
sudo adduser --system --group --shell /bin/false --home /opt/ilo_exporter iloexporter

# move
sudo mv ilo_exporter /opt/ilo_exporter/exporter

# permissions
sudo chown -R root:root /opt/ilo_exporter
sudo chmod 0755 /opt/ilo_exporter

# venv
sudo apt install python3-venv
sudo python3 -m venv /opt/ilo_exporter/venv
source /opt/ilo_exporter/venv/bin/activate
sudo pip install prometheus_client pysnmp requests
```

#### if using python >= 3.12:
*asyncore, a dependency of pysnmp, was removed in python 3.12.*

```bash
sudo pip install pyasyncore
```

#### if also using HTTPS:
```bash
sudo touch /opt/ilo_exporter/ilo_credentials
sudo chmod 0750 /opt/ilo_exporter/ilo_credentials

# replace 'vim' with your editor of choice
sudo vim /opt/ilo_exporter/ilo_credentials
```
Add these contents, making sure to replace `$USERNAME` and `$PASSWORD` with the credentials you picked in step 3 of [HTTPS server setup](#https-optional)
```bash
ILO_USERNAME="$USERNAME"
ILO_PASSWORD="$PASSWORD"
# uncomment and point to an SSL certificate if you have one
#ILO_CERTIFICATE="/path/to/ssl/certificate.pem"
```


### test
make sure it works

```bash
python /opt/ilo_exporter/exporter/main.py --help

python /opt/ilo_exporter/exporter/main.py -i $ILO_ADDRESS -c $SNMP_COMMUNITY -v
```

### systemd service
Make sure to replace 
- `$ILO_ADDRESS` with your ILO controller address, and
- `$ILO_COMMUNITY` with the community you picked in step 3 of [SNMP server setup](#snmp)
```bash
cat << 'EOF' | sudo tee /etc/systemd/system/ilo-exporter.service
[Unit]
Description=A fast(er) prometheus exporter for applicable HP servers using SNMP via the ILO controller.
After=network-online.target

[Service]
User=iloexporter
# uncomment if using HTTPS
#EnvironmentFile=/opt/ilo_exporter/ilo_credentials
WorkingDirectory=/opt/ilo_exporter/exporter
# add --https-fans and/or --https-temperature to this to use HTTPS
ExecStart=/opt/ilo_exporter/venv/bin/python -u /opt/ilo_exporter/exporter/main.py -i $ILO_ADDRESS -c $ILO_COMMUNITY
Restart=on-failure
KillMode=process

# security
PrivateTmp=true
ProtectHome=true
ProtectSystem=strict
PrivateDevices=true
NoNewPrivileges=true
CapabilityBoundingSet=~CAP_SYS_ADMIN

[Install]
WantedBy=multi-user.target
EOF

sudo systemctl daemon-reload
```

```bash
# enable
sudo systemctl enable --now ilo-exporter

# check status
sudo systemctl status ilo-exporter

# test
curl localhost:6969

# monitor logs
sudo journalctl -xefu ilo-exporter
```

### updating
Grab the latest release from the [releases tab](https://github.com/Benjamin-Wiegand/ilo_exporter/releases).
Replace `$DOWNLOAD_URL` with the appropriate download url.

```bash
cd ~
curl $DOWNLOAD_URL -Lo ilo_exporter.tar.gz

# extract
tar -xvf ilo_exporter.tar.gz
rm ilo_exporter.tar.gz

# replace old version
sudo rm -rf /opt/ilo_exporter/exporter
sudo mv ilo_exporter /opt/ilo_exporter/exporter

# restart exporter
sudo systemctl restart ilo-exporter

# check status
sudo systemctl status ilo-exporter
```

## Prometheus configuration
nothing too special
```yaml
  - job_name: some-ilo
    static_configs:
      - targets: ['your-ilo-exporter:6969']
```
