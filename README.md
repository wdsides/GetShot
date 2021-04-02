# GetShot
Python program that searches for nearby COVID vaccine appointments at CVS, Walgreens, and Safeway (Albertsons), with optional SMS text notifications.

Disclaimer:
This code is provided 'as-is'. See license for full disclaimer. This code was thrown together very quickly and carelessly with little regard to readability or style, and with very little debugging. It may work fine for other users/locations, it may wipe your hard drive, or it may explode. I haven't tested it, I don't know. It almost certainly won't work outside the US. 

All searches are done via HTTP requests to web endpoints. They are valid as of 4/2/2021, but may stop working in the future, breaking the code unless and until a valid endpoint can be found.

You will need two (free) third-party accounts for this code to work properly: Twilio (to send text notifications) & opencagedata.com (to provide location decoding services). Enter your API keys and phone number into the private_API_keys.py file. 

Configuration:
In addition to copying your API keys into the private_API_keys.py file as mentioned above, there are a few options you can set near the top of the main VaccineAvailability.py file that you can configure, this should be self explanatory.

All dependencies can be easily installed with pip.
