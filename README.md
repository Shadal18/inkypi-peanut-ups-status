# inkypi-peanut-ups-status

PeaNUT UPS Status plugin for InkyPi.

This plugin displays UPS status information on an InkyPi display using a PeaNUT device API endpoint. It is a **PeaNUT-only** plugin, so the InkyPi device does not need the NUT client tools installed locally; PeaNUT handles the UPS data and exposes it over HTTP [web:3].

## Plugin details

- Repository name: `inkypi-peanut-ups-status`
- Plugin ID: `peanut_ups_status`
- Python class: `PeaNUT`

## Features

- Pulls live UPS data from a PeaNUT device API endpoint.
- Displays UPS status such as Online or On Battery.
- Shows battery percentage.
- Shows runtime remaining.
- Shows UPS load percentage.
- Optionally shows input voltage.
- Optionally shows output voltage.
- Optionally shows battery voltage.

## Requirements

- A working InkyPi installation with plugin support.
- A reachable PeaNUT instance on your network.
- A working PeaNUT device endpoint for your UPS.

## Install

```bash
inkypi plugin install peanut_ups_status https://github.com/shadal18/inkypi-peanut-ups-status
```

## Update

```bash
cd ~/InkyPi/src/plugins/peanut_ups_status
git pull origin main
sudo systemctl restart inkypi.service
```

## Configuration

Open the plugin settings in InkyPi and set the PeaNUT device URL.

Example:

```text
http://docker-host.lan:8080/api/v1/devices/cyberups
```

If your UPS device id is `ups`, the URL may look like this:

```text
http://docker-host.lan:8080/api/v1/devices/ups
```

The device portion of the URL should match the UPS identifier exposed by PeaNUT for that device endpoint [web:3].

## Display options

You can show or hide the following fields:

- Battery
- Runtime
- Load
- Input Voltage
- Output Voltage
- Battery Voltage

## Troubleshooting

### Plugin does not load

Restart the InkyPi service after installing or updating the plugin:

```bash
sudo systemctl restart inkypi.service
```

InkyPi plugin registration uses `plugin-info.json` with `display_name`, `id`, and `class`, and the Python file should match the plugin directory name [web:3].

### PeaNUT request timeout

If the plugin times out, verify that the InkyPi device can reach the PeaNUT server over the network:

```bash
curl -v http://docker-host.lan:8080/api/v1/devices/cyberups
```

If hostname resolution fails, try using the server IP address instead of the hostname.

### Invalid JSON or empty response

Test the PeaNUT device URL directly in a browser or with `curl` and confirm that it returns JSON for a UPS device endpoint.

### Wrong UPS shown

Make sure the last path segment in the URL matches the correct PeaNUT device id for your UPS.

## Repository

[https://github.com/shadal18/inkypi-peanut-ups-status](https://github.com/shadal18/inkypi-peanut-ups-status)
