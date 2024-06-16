# sustainability-scanner

Sustainability is one of our key focus passions at [NewsoftSage](https://newsoftsage.co.uk/). Building on the amazing work of awslabs we wanted to package up their [sustainability-scanner](https://github.com/awslabs/sustainability-scanner) in a ready to use container.

If you use CloudFormation and would like to know more about how NewsoftSage can help you meet your sustainability targets then please get in touch.

![](https://github.com/newsoft-sage/sustainability-scanner/blob/main/doc/sus.gif)

## Building

If you wish to build our docker image locally you can clone our repo and use the following.

```
docker build -t sustainability-scanner .
```

## Running

Once built you simply run the container and mount your CloudFormation directory to `/templates/`

```
docker run --rm -v $(pwd)/examples/:/templates/ sustainability-scanner
```

## Consulting

If you are interested in finding out more about how Newsoft Sage can help you meet your sustainability targets please [get in touch](https://newsoftsage.co.uk/contact/) or [visit our website](https://newsoftsage.co.uk/) to find out more.
