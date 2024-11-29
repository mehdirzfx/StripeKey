# Stripe API Key Checker

## Overview

This Python script is designed to check the validity of Stripe API keys. It generates random API keys with a specified prefix and length, sends requests to the Stripe API to check if the generated keys are valid, and reports valid keys through a Telegram bot.

## Features

- **Concurrent Execution**: Runs multiple threads to check API keys concurrently.
- **Telegram Notifications**: Sends notifications to a specified Telegram chat when a valid key is found.
- **Customizable Parameters**: Allows users to specify the number of threads, key length, and key prefix through command-line arguments.

## Prerequisites

- Python 3.x
- Required libraries:
  - `requests`
  - `colorama`

To install the required libraries, create a `requirements.txt` file in your project directory with the following content:

```
pip install -r requirements.txt
```

## Configuration

Before running the script, configure the following settings in the script:
- **Telegram Bot**:
  - Replace `<TOKEN>` with your Telegram bot token.
  - Replace `<CHAT_ID>` with your Telegram chat ID.
  - Replace `<ID>` with your Telegram topic ID (optional).

## Script Usage

### Command-Line Arguments

- `-t` (int): Number of concurrent threads to use. Default is 30.
- `-l` (int): Length of the generated API key. Default is 36.
- `-s` (str): Prefix for the generated API key. Default is `"sk_live"`.

### Example Usage

To run the script with the default configuration (30 threads, 36-character API keys, prefix "sk_live"):

```
python main.py
```

To specify custom values, such as 50 threads, 32-character keys, and a prefix of `"sk_test"`:

```
python main.py -t 50 -l 32 -s sk_test
```

### Script Execution

1. The script generates API keys with the specified length and prefix.
2. It then checks the validity of each key by sending a request to the Stripe API.
3. If a valid key is found (HTTP status 200), it is logged and a message is sent to the Telegram chat.
4. Invalid keys or errors are logged with appropriate messages.
5. This process continues indefinitely, checking new keys and sending updates.

## Important Notes

- **Rate Limits**: Be mindful of Stripe's rate limits when running the script with many threads.
- **Security**: Ensure the API keys generated and used are handled securely and responsibly.
