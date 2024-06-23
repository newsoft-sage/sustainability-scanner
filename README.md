# sustainability-scanner

Sustainability is one of our key focus passions at [NewsoftSage](https://newsoftsage.co.uk/). The [Sustainability Pillar](https://docs.aws.amazon.com/wellarchitected/latest/sustainability-pillar/best-practices-for-sustainability-in-the-cloud.html) of the AWS Well-Architected Framework is one of the cornerstones of understanding and improving your carbon footprint and sustainability impact when using the AWS Cloud.

Building on the amazing work of awslabs we wanted to package up their [sustainability-scanner](https://github.com/awslabs/sustainability-scanner) in a ready to use, simple to consume Docker container. You can use this in your local development environment or fully integrated into your Continuous Integration/Continuous Delivery (CICD) pipelines.

If you use the AWS Cloud, CloudFormation, Serverless Application Model (SAM) or Cloud Development Kit (CDK) and would like to know more about how NewsoftSage can help you meet your sustainability targets then please get in touch.

![](https://github.com/newsoft-sage/sustainability-scanner/blob/main/doc/sus.gif)

## Running

Our Docker Image is available pre-built in our [public repository](https://gallery.ecr.aws/d5s0w9y8/sustainability-scanner) so you simply run a container and mount your CloudFormation directory to `/templates/`. You can also mount a directory to `/output/` to retrieve the reports for further ana

```
docker run --rm -v $(pwd)/examples/:/templates/ -v $(pwd)/output:/output/ public.ecr.aws/d5s0w9y8/sustainability-scanner
```

## Building

If you wish to build our docker image locally you can clone our repo and use the following.

```
docker build -t sustainability-scanner .
```

## Consulting

If you are interested in finding out more about how Newsoft Sage can help you meet your sustainability targets please [get in touch](https://newsoftsage.co.uk/contact/) or [visit our website](https://newsoftsage.co.uk/) to find out more.
