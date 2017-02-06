#Docker PaaS Roadmap

2017 Q1

- Postgres Master/Slave backend
- Dynamic storage backend (infinit.io integration)
- EFS mount to volume for static images (app trigger to use local images if necessary) 
- Use Jmeter to hit applications and show off CPU and mem limits and also good for demonstrating high availability (what is the error rate when a node dies)
- SNI/HTTPS with HRM
- GUI button to simulate app health check failure

**Stretch Goals**

- Application transactions self monitoring and autoscaling
- Rebase on to more robust application stack (Liberty, Springboot, etc.)
- Updates for future versions of DDC & Docker Engine


#"How to Demo DDC" Topics for Documentation
**Basic**

- Compose deployment of app on D4M and DDC
- Overlay networking at work
- Scaling a service
- Health checks & container lifecycle management
- Secrets
- Rolling update & rollback

**Advanced**

- Show application under load with Jmeter
- Show application under load and recovery after killing node
- Blue/Green deployment with DDC
- SNI/HTTPS with HRM
- Application Autoscaling 



#Release Notes
#####v1.0
- Voting page with three options
- Admin page with voting results
- HA Consul backend
- Secrets-protected Admin Console page
- Sticky admin sessions
- Toggleable health checks

