# pynator
 Python wrapper for Emailnator and SMSNator

<a href='https://ko-fi.com/hackirby'><img src='https://storage.ko-fi.com/cdn/kofi3.png' width=150></a>

simple wrapper for emailnator.com and smsnator.online services, allowing you to generate disposable email addresses and phone numbers. It provides a convenient way to interact with the emailnator.com and smsnator.online APIs using Python.

## Features
* Generate disposable email addresses/phone numbers with customizable options.
* Retrieve a list of messages from a disposable email address/phone number.
* Retrieve the content of a specific email/phone message.

## Installation:
You can install the pynator library using pip:
```sh
pip install pynator
```

## Usage
Here's a basic example of how to use the pynator library to generate an email address:


```py
from pynator import EmailNator

# Initialize the EmailNator client
client = EmailNator()

# Generate a disposable email address
email = client.generate_email()

# Get a list of messages for the generated email address
messages = client.get_messages(email)

# Print the messages
for message in messages:
    print(message)
    print(client.get_message(email, message.message_id)) # print message text
```

And a basic example of how to use the pynator library to generate a phone number:
```py
from pynator import SMSNator

# Initialize the SMSNator client
client = SMSNator()

# Generate a disposable phone number
email = client.generate_number()

# Get a list of messages for the generated phone number
messages = client.get_messages(email)

# Print the messages
for message in messages:
    print(message)
    print(message.message) # print message text
```

## License
This library is released under the MIT License.

## Contributing
Contributions to this project are welcome! Feel free to open issues, submit pull requests, or suggest improvements.

## Contact
If you have any questions or need further assistance, please contact [@hackirby:matrix.org
](https://matrix.to/#/@hackirby:matrix.org)