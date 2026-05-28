# inkypi-peanut-ups-status

A PeaNUT-only UPS status plugin for InkyPi that displays battery charge, runtime, load, and voltage data from a PeaNUT device API endpoint.

## Plugin details

- Repository name: `inkypi-peanut-ups-status`
- Plugin ID: `peanut_ups_status`
- Python class: `PeaNUT`

## Features

- Pulls live UPS data from a PeaNUT device endpoint
- No NUT client installation required on the InkyPi device
- Displays UPS status such as Online or On Battery
- Shows battery percentage
- Shows runtime remaining
- Shows UPS load
- Optional input voltage display
- Optional output voltage display
- Optional battery voltage display

## Requirements

- A working InkyPi installation with plugin support
- A reachable PeaNUT instance on your network
- A working PeaNUT device API endpoint for your UPS

## Install

Install the plugin using the InkyPi plugin installer:

```bash
inkypi plugin install peanut_ups_status https://github.com/shadal18/inkypi-peanut-ups-status
```

## Update

To update the plugin on your InkyPi device:

1. SSH into your InkyPi host.
2. Change into the plugin directory:
   ```bash
   cd ~/InkyPi/src/plugins/peanut_ups_status
   ```
3. Pull the latest changes and restart InkyPi:
   ```bash
   git pull origin main && sudo systemctl restart inkypi.service
   ```

## Setup

Open the plugin settings in InkyPi and enter your PeaNUT device API URL.

Example:

```text
http://docker-host.lan:8080/api/v1/devices/cyberups
```

If your UPS is named `ups` in NUT/PeaNUT, the URL may look like:

```text
http://docker-host.lan:8080/api/v1/devices/ups
```

The device portion of the URL is the UPS device identifier configured in NUT and exposed by PeaNUT [web:600][web:629].

## Display options

You can show or hide:

- Battery
- Runtime
- Load
- Input Voltage
- Output Voltage
- Battery Voltage

## Troubleshooting

### Timeout while querying PeaNUT

If the plugin times out, the InkyPi host likely cannot reach the PeaNUT server even if your desktop browser can.

Check connectivity from the InkyPi device:

```bash
curl -v http://docker-host.lan:8080/api/v1/devices/cyberups
```

If hostname resolution is the issue, use the server IP instead of `docker-host.lan`.

### Invalid JSON or empty response

Open the PeaNUT device URL in a browser or with `curl` and verify that it returns UPS JSON data.

## Repository

[https://github.com/shadal18/inkypi-peanut-ups-status](https://github.com/shadal18/inkypi-peanut-ups-status)
