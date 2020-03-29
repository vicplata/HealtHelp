# HealtHelp
Twilio Bot to help hospitals and patients

This project was designed to try to help hospitals during the corona vairus pandemic. 

I am from Mexico and today (03/28/2020) Mexico has only 1% of covid-19 cases compared to the US. On a personal story:
  A couple from Mexico were living their normal lifes, three days ago the husband got some symptoms that could
  potentially be coronavirus symptoms. He went to the hospital and that is the last thing his wife knows about him. 
  It has been 3 days already, she is not addmitted into the hospital, and the hospital is so busy that they don't even
  answers calls. With that story on mind I decided to create a programm that could help hospitals, patients and 
  family members.
  
  
  
This project uses Twilio autobot, to process sms and calls from a potential patient's family member. It has one main fucntion
and two smaller functions.

1.Checking on a patient's status
  via sms or voice call a family member can get a patient's info. Always keeping the information secure. The family member has
  to be on a list of allowed users and also has to provide a secure code. The user will ask for a patient info via the Twilio bot.
  They will need to provide the patients name, their name and the secure code. 
  
2.Checking symptoms
  via sms and voice call the bot will give a recommendation based on the symptoms the user is having.
  
3.Get stadistics
  via sms and voice call the user can get the daily and total cases in the us. Using APIs updated daily by the WHO.
  
  
  Twilio uses json to generate data requests. The program that I coded in python will process those requests and provide
  the user the info neede. 
  
   def collect():
      will recive the patients name, the users name, and the secure code which will be hashed. It will search for the patient
      If a patient is found it will return the patient's info. 
   
   def collectsyn():
      will recieve a list os symptons that the Twilio both gathered from the user and respond with a recommendation.
   
   def collectStats():
      will return the daily and total number of cases in the US.
      
      
 I used ngrok to tunnel my localhost. 
  
