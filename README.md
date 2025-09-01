Tuya Utilities for controlling Tuya Smart Things

## Scripts

### `devicelist.py`
Lists all Tuya devices associated with your account. Displays device names, IDs, and local keys for each device.
```bash
python scripts/devicelist.py
```

### `example.py`
Interactive script for testing Tuya device API endpoints. Allows you to make GET or POST requests to specific device endpoints by entering the device ID and endpoint interactively. Also includes an example of sending commands to a specific device.
```bash
python scripts/example.py
```

### `getdetails.py`
Retrieves detailed information about a specific Tuya device. Prompts for a device ID and returns the device's local key and other details.
```bash
python scripts/getdetails.py
```

### `getkey.py`
Gets the local key for a specific Tuya device. Continuously prompts for device IDs and returns their corresponding local keys.
```bash
python scripts/getkey.py
```

## Requirements
- Python 3.x
- `requests` library
- Valid Tuya Cloud Development credentials (client_id and secret)