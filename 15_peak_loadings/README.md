Describe solution that solves peak loadings problem for biggest european football website https://goal.com  

- Analyze all types of pages on the site
- Analyze  and list possible sources of peak loadings
- Describe possible solution for each type 


## Page Types

- News feed
- Static content 
- Playes information
- Match results
- Live scores


## Peek Loading Sources

- Concurrent resources usage (main page/hot news/...)
- Bot activity
- Short polling (Live scores)
- External attacks

## Solutions

***Schedule***
- Preparation for championships and matches according to the schedule. Allocate resources to specific regions when matches are played there. Or dynamically scale resources during championship matches.

***Caching***
- Everything that is on the main page. Because there is no personalization for users, this is easy to do.
- Hot news. News from the main page and news from the last days. You can also track requests for older news. 

***Load Balancer configuration***
- To reduce the load from bots, create rules on the balancer that let bots pass with a certain frequency, the content of which is updated frequently on pages. 

***CDN***
- Use CDN caching for static content 

***DDoS***
- Use existing protection tools like Cloudflare 
