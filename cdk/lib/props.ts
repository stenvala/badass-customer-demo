import * as s3 from "aws-cdk-lib/aws-s3";
import * as events from "aws-cdk-lib/aws-events";
import { CustomDomainNameFactory } from "./custom-domain-name.factory";

export type Stage = "dev" | "qa" | "prod";

export interface CdkProps {
  env: {
    account: string;
    region: string;
    stage: string;
  };

  stackSuffix: string;

  domainNameFactory?: CustomDomainNameFactory;

  constructs: {
    artifactsBucket?: s3.Bucket;
    bus?: events.EventBus;
  };
}
