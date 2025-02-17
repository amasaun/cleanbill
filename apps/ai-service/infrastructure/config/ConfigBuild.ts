import { App, Environment, RemovalPolicy } from "aws-cdk-lib"

import { Config } from "./Config"
import { Parameters } from "./Parameters"

type SsmParameter = {
  [key: string]: string
}

export enum StackStage {
  EPHEMERAL = "eph",
  PROOF_OF_CONCEPT = "poc",
  INTEGRATION = "int",
  STAGING = "stg",
  PRODUCTION = "prod",
}

export type ConfigBuild = {
  readonly serviceName: string
  ssmParameters: SsmParameter
  readonly env?: Environment
  readonly envVariables: { readonly [key: string]: string }
  readonly prefix: string | undefined
  readonly stage: StackStage
  removalPolicy: RemovalPolicy
}

/**
 * Helper method to retrieve `prefix` if passed in the app's context.
 * `cdk deploy --context prefix=a_name`
 * @param app
 * @returns prefix value or undefined.
 */
export const getContextPrefix = (app: App): string => {
  return app.node.tryGetContext("prefix") || ""
}

/**
 * Helper method to retrieve `stage` if passed in the app's context.
 * `cdk deploy --context stage=eph`
 * @param app
 * @returns stage value or undefined.
 */
export const getContextStage = (app: App): string => {
  const contextStage = app.node.tryGetContext("stage")
  if (
    contextStage &&
    Object.values(StackStage).includes(contextStage as StackStage)
  ) {
    return contextStage
  }

  return StackStage.EPHEMERAL
}

export const buildEnvironment = (app: App) => {
  console.log(
    `aws pipeline region - account environment ${process.env.REGION} - ${process.env.ACCOUNT}`
  )

  const stage = getContextStage(app) as StackStage
  let jsonSettings = Config.environments[stage]

  if (stage === StackStage.EPHEMERAL)
    jsonSettings = ephBuildEnvironment(app, jsonSettings)

  const settings: ConfigBuild = {
    serviceName: Config["serviceName"],
    envVariables: jsonSettings,
    ssmParameters: Parameters,
    env: {
      account: process.env.ACCOUNT,
      region: process.env.REGION,
    },
    prefix: getContextPrefix(app),
    stage,
    removalPolicy: jsonSettings.removalPolicy,
  }

  console.log("Settings", settings)

  return settings
}

export const ephBuildEnvironment = (
  app: App,
  jsonSettings: (typeof Config.environments)[StackStage]
) => {
  const prefix = getContextPrefix(app)

  // Create a mutable copy of jsonSettings
  const mutableSettings = { ...jsonSettings }

  // Use prefix if it exists, otherwise use StackStage.EPHEMERAL
  const replacementValue = prefix || StackStage.EPHEMERAL

  mutableSettings.eventBus = mutableSettings.eventBus.replace(
    "{prefix}",
    replacementValue
  )
  mutableSettings.centralApi = mutableSettings.centralApi.replace(
    "{prefix}",
    replacementValue
  )

  // Return or use the modified copy as needed
  return mutableSettings
}
