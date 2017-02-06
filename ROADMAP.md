#Docker PaaS Roadmap

2017 Q1

- Postgres Master/Slave backend
- Dynamic storage backend (infinit.io integration)
- EFS mount to volume for static images (app trigger to use local images if necessary) 
- Use Jmeter to hit applications and show off CPU and mem limits and also good for demonstrating high availability (what is the error rate when a node dies)
- SNI/HTTPS with HRM

**Stretch Goals**

- Application transactions self monitoring and autoscaling
- Rebase on to more robust application stack (Liberty, Springboot, etc.)
- Updates for future versions of DDC & Docker Engine


#DDC Doc Examples Roadmap
- Show application under load
- Show application under load after killing node
- Blue/Green deployment with DDC
- Rolling updates & rollback with DDC
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

