## Deployment

```
docker build -t flask .
docker run -p 5000:5000 flask

```

## (01) Setup kubectl

## a. Download kubectl version 1.20

## b. Grant execution permissions to kubectl executable

## c. Move kubectl onto /usr/local/bin

## d. Test that your kubectl installation was successful

```
curl -o kubectl https://amazon-eks.s3.us-west-2.amazonaws.com/1.19.6/2021-01-05/bin/linux/amd64/kubectl

chmod +x ./kubectl

sudo mv ./kubectl /usr/local/bin

kubectl version --short --client

```

## (02) Setup eksctl

## a. Download and extract the latest release

## b. Move the extracted binary to /usr/local/bin

## c. Test that your eksclt installation was successful

```
curl --silent --location "https://github.com/weaveworks/eksctl/releases/latest/download/eksctl_$(uname -s)_amd64.tar.gz" | tar xz -C /tmp

sudo mv /tmp/eksctl /usr/local/bin

eksctl version

```

## (03) Create an IAM Role and attache it to EC2 instance

## Note: create IAM user with programmatic access if your bootstrap system is outside of AWS

## create group -> Give Administrator access

## IAM user should have access to

## IAM

## EC2

## VPC

## CloudFormation

## Now go to mobxterm and execute the following commands

## aws configure ( This will ask the aws credentials )

## (04) Create your cluster and nodes

```
eksctl create cluster --name cluster-name  \
--region region-name \
--node-type instance-type \
--nodes-min 2 \
--nodes-max 2 \
--zones <AZ-1>,<AZ-2>
```

## example: (run this )

```
 eksctl create cluster --name tharindu-cluster-4 --node-type t3.small --zones eu-north-1a,eu-north-1b,eu-north-1c


```

### To get the external ip address of our cluster

```
kubectl get services -o wide
```

## \*\*\* Now in aws console -> CloudFormation -> Over here you can see the cluster that we created

## Delete the cluster

```
eksctl delete clustr tharindu-cluster-6
```
