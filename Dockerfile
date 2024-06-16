FROM public.ecr.aws/aws-cloudformation/cloudformation-guard:latest

RUN apk add --no-cache python3 py3-pip bash
RUN pip3 install sustainability-scanner --break-system-packages
RUN mv /usr/src/cloudformation-guard/cfn-guard /usr/local/bin/

COPY entrypoint.sh .
RUN chmod +x ./entrypoint.sh
ENTRYPOINT ["./entrypoint.sh"]
CMD ["/templates/"]
