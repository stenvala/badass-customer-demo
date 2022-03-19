import * as cdk from "aws-cdk-lib";
import * as lambda from "aws-cdk-lib/aws-lambda";
import { CdkProps } from "./props";
import * as log from "aws-cdk-lib/aws-logs";
import * as apigw from "aws-cdk-lib/aws-apigateway";

export class ApiLambda {
  constructor(scope: cdk.Stack, props: CdkProps) {
    const lambdaFun = new lambda.Function(scope, "ApiLambda", {
      runtime: lambda.Runtime.PYTHON_3_8,
      code: lambda.Code.fromAsset("../api"),
      handler: "main.handler",
      logRetention: log.RetentionDays.ONE_DAY,
      environment: {
        AWS: "true",
      },
      timeout: cdk.Duration.seconds(30),
      architecture: lambda.Architecture.ARM_64,
    });

    const api = new apigw.LambdaRestApi(scope, "ApiGw", {
      handler: lambdaFun,
      proxy: true,

      defaultCorsPreflightOptions: {
        allowCredentials: true,
        allowHeaders: [
          "Content-Type",
          "X-Amz-Date",
          "Authorization",
          "X-Api-Key",
        ],
        allowOrigins: apigw.Cors.ALL_ORIGINS, // Edit this when there is UI stack
        allowMethods: apigw.Cors.ALL_METHODS,
      },
    });

    new cdk.CfnOutput(scope, "APIAWSUrl", { value: api.url });
  }
}
