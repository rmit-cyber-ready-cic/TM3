# TM3
Cloud Innovation Centre at RMIT University powered by AWS

Team TM3



**Problem Statement:**
"How might we educate time poor SMBs to be cyber secure?"
 



**Solution:**
	Armour-1 - A real time anomaly detector, helps you find out the abnormal activities within your online business which might be making your business predisposed to cyber-attacks and helps you fight back at it.  How does it do that? It detects abnormal activities with the online business portal by implementing advance machine learning models to detect any abnormal pattern in the system’s network logs (network reports) and provide reports with lucid visualizations. 



**Use Cases:**
- Increase in error rates
- Sudden/ Irregular change in user location
- Unusual amount of data flow (Download/Upload)
- Increased access at odd time of day
- Increased in network level traffic rejections
- Detected malicious visits cause network congestion
- Identify suspicious behavior



**Features:**

   - Automatically extracts all the required (network related) information from your system and hands it over to the anomaly detector. 
   - Visualizations of suspicious activities which are easy to compare and understand.
   - Can work with both - Historic and Live data


**Installation Steps**


- Watch the demo video and ppt (Refer Case Study @ https://www.rmit.edu.au/for-business/activator/partnerships/cloud-innovation-centre) to understand the functionality of the application.
- Use 'CFN_elasticSearch.yaml' file to create an elasticsearch domain in your AWS account.
- Run python script with the elastic search endpoint url, master username and password. Replace the new elasticsearch domain endpoint and master userID and password.
- After the above step, mock logs will be uploaded successfully into ES domain and can be visualised using Kibana.

