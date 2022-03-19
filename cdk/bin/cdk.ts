#!/usr/bin/env node
import "source-map-support/register";
import * as cdk from "aws-cdk-lib";
import { AppStack } from "../lib/app.stack";
import { Stage } from "../lib/props";
const fs = require("fs");

const app = new cdk.App();

const env = JSON.parse(fs.readFileSync("env.json"));

const stage = env["stage"] as Stage;
new AppStack(app, {
  env: {
    account: process.env.CDK_DEFAULT_ACCOUNT!,
    region: process.env.CDK_DEFAULT_REGION || "eu-west-1",
    stage,
  },
  stackSuffix: `-${env.stackSuffix}`,
  constructs: {},
});
