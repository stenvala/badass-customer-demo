import { Stack } from "aws-cdk-lib";
import { Construct } from "constructs";
import { CdkProps } from "./props";
import { ApiLambda } from "./api.lambda";
import { getResourceSuffix } from "./utils";

export class AppStack extends Stack {
  constructor(scope: Construct, props: CdkProps) {
    super(scope, `BADASS-CUSTOMER-DEMO${getResourceSuffix(props)}`, {
      env: props.env,
    });

    new ApiLambda(this, props);
  }
}
