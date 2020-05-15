# Pull and start Jenkins server
docker pull jenkins/jenkins:lts-alpine
# Get docker group ID
GID=`getent group docker|cut -d: -f3`
# Start Jenkins and get its container ID
REGION=`curl -s http://169.254.169.254/latest/dynamic/instance-identity/document|grep region|awk -F\" '{print $4}'`
CID=`docker run --log-driver=awslogs --log-opt awslogs-region=${REGION} --log-opt awslogs-group=/aws/ec2/a205890-jenkins -d --name jenksinci -p 8080:8080 -v /var/run/docker.sock:/var/run/docker.sock -v /efs/jenkins:/var/jenkins_home jenkins/jenkins:lts-alpine`
# Add docker permissions to Jenkins
docker exec -i --user root ${CID} addgroup -g ${GID} docker
docker exec -i --user root ${CID} apk add shadow docker
docker exec -i --user root ${CID} usermod -aG docker jenkins
# Install required plugins
docker exec -i ${CID} /usr/local/bin/install-plugins.sh ws-cleanup durable-task gitlab-plugin github workflow-job workflow-aggregator workflow-multibranch ldap git-client docker-plugin ansicolor blueocean credentials
# Restarting Jenkins container (otherwise it won't be able to use Docker)
docker restart ${CID}


