#!/usr/bin/env node
import { App } from "aws-cdk-lib"
import { buildEnvironment } from "../config/ConfigBuild"
import { TagHelper } from "../config/Tags"
import { AuthStack } from "../stacks/AuthStack"
import { IngestionStack } from "../stacks/IngestionStack"
import { LayerStack } from "../stacks/LayersStack"

// build steps, app pre requirements setup
const app = new App()
const appSettings = buildEnvironment(app)
const baseStackName =
  `${appSettings.prefix}-${appSettings.serviceName}-${appSettings.stage}`
    .trim()
    .toLowerCase()
    .replace(/^-/, "") // remove leading hyphen if prefix is empty
// end of build steps

// add required tags to the stacks, if you have required tags, please add here
const requiredTags = [
  {
    key: "service",
    value: appSettings.serviceName,
  },
  {
    key: "AppManagerCFNStackKey",
    value: baseStackName,
  },
]
TagHelper.addTags(app, requiredTags)
// end of adding tags

// this session is for stack definition
const layerStack = new LayerStack(app, "LayerStack", {
  stackName: baseStackName.concat("-layers"),
  env: appSettings.env,
  appSettings: appSettings,
})

const serviceAuthStack = new AuthStack(app, "ServiceAuth", {
  stackName: baseStackName,
  env: appSettings.env,
  appSettings: appSettings,
})
serviceAuthStack.addDependency(layerStack)

const ingestionStack = new IngestionStack(app, "IngestionStack", {
  stackName: baseStackName.concat("-ingestion"),
  env: appSettings.env,
  appSettings: appSettings,
})
ingestionStack.addDependency(serviceAuthStack)
//end of session stack definition
