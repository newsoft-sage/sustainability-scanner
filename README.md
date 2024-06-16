# sustainability-scanner

Sustainability is one of our key focus areas at NewsoftSage. Building on the amazing work of awslabs we wanted to package up their [sustainability-scanner](https://github.com/awslabs/sustainability-scanner) in a ready to use container.

If you use CloudFormation and would like to know more about how NewsoftSage can help you meet your sustainability targets then please get in touch.

## Building

If you wish to build our docker image locally you can clone our repo and use the following.

```
docker build -t sustainability-scanner .
```

# Running

Once built you simply run the container and mount your CloudFormation directory to `/templates/`

```
docker run --rm -v $(pwd)/examples/:/templates/ sustainability-scanner
```
