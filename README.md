# Stripe Product Deletion Automation

Automate the process of deleting archived products on the Stripe dashboard using Selenium WebDriver.


## Motivation

Stripe doesn't provide an API to delete archived products, requiring manual deletion through the dashboard. As engineers, we aim to streamline repetitive tasks during development and testing, saving valuable time. This script provides a solution by automating product deletion, running seamlessly in the background (headless).

## Prerequisites

Before you begin, ensure you have met the following requirements:
- Python installed on your local machine.
- Selenium library (`pip install selenium`).
- Chrome WebDriver installed and added to your system's PATH.

## Installation

1. Clone this repository to your local machine:
   ```shell
   git clone https://github.com/MilovanTomasevic/stripe-product-deletion.git
   cd stripe-product-deletion
   ```

2. Enter your Stripe dashboard login credentials:
    ```py
    USER_EMAIL = "your_email@example.com"
    USER_PASSWORD = "your_password"
    ```

3. Run the script:
    ```sh
    python main.py
    ```

The script automates the deletion of archived products on the Stripe dashboard, eliminating the need for manual intervention.


## Future Enhancements

There is room for improvement in this solution. Feel free to contribute or suggest enhancements to make this automation even more effective.
