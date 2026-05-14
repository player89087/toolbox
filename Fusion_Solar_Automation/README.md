## Automation script for FusionSolar Systems

This script is only tested to work with Huawei inverter aswell as Huawei Battery,
 all of it managed by FusionSolar. Wether it works with something else I dont know.
 Currently it checks the production as well as the soc (state of charge) of the battery,
 depending on the criteria that was given the script sends out a notification to a WhatsApp Group, that the current electricity
is enough for a certain task.  This project was given up, as I faced major difficulties. 
How if you want to use it. 

**1 Check Domain** If your inside the EU it is highly possible that your accesing FusionSolar through a domain like uni003eu5.org 
you can check when you access the FusionSolar website. If that is the case you need to change l.84 
*client = FusionSolarClient("user", "password", huawei_subdomain="uni003eu5"*
to the domain that is displayed in the URL of the FusionSolar website. 
**2 Automatic Text Input** This project was entirely devolped for the RasberryPi. On there it is proven to work, with RasberryPiOS. 
If that is not the case for you you should probably 'xdottool' then it should work. 
**3 Multiple Plants** If you should own multiple power plants you need to rewrite the whole get_data with an loop, as it currently
just checks one plant. 
**4 Adjust Parameters** I've commented every line where you need to enter you parameters your credentials. 


Please note that you don't need to create an seperate API account for this, you can just put your regular credentials from 
FusionSolar. 
