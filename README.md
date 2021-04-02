# GetShot
Python program that searches for nearby COVID-19 vaccine appointments at CVS, Walgreens, and Safeway (Albertsons), with optional SMS text notifications.

Disclaimer:
This code is provided 'as-is'. See license for full disclaimer. This code was thrown together very quickly and carelessly with little regard to readability or style, and with very little debugging. It may work fine for other users/locations, it may wipe your hard drive, or it may explode. I haven't tested it, I don't know. It almost certainly won't work outside the US. 

All searches are done via HTTP requests to web endpoints. They are valid as of 4/2/2021, but may stop working in the future, breaking the code unless and until a valid endpoint can be found.

You will need two (free) third-party accounts for this code to work properly: Twilio (to send text notifications) & opencagedata.com (to provide location decoding services). Enter your API keys and phone number into the private_API_keys.py file. 

Configuration:
In addition to copying your API keys into the private_API_keys.py file as mentioned above, there are a few options near the top of the main VaccineAvailability.py file that you should configure, particularly your location - these should be self explanatory.

All dependencies can be easily installed with pip.

Running the code:
This program will run indefinitely as long as you let it. It searches all three pharmacies every two minutes. It's fairly verbose in the console. If textNotifications=True, it will send SMS notifications to your phone when it finds a nearby availability, with a link to sign up. It will only send a limited number SMS notifications per session, so that it will not spam your phone too much if a lot of appointments open up. To reset the counter, restart the code. 
