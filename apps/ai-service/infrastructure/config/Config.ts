import { RemovalPolicy } from "aws-cdk-lib"
import { StackStage } from "../config/ConfigBuild"

type Config = {
  readonly serviceName: string
  readonly environments: {
    [K in StackStage]: {
      readonly envName: string
      readonly centralApi: string
      readonly eventBus: string
      readonly removalPolicy: RemovalPolicy
    }
  }
}

export const Config: Config = {
  // Never modify this parameters, unless you tested all the environments
  serviceName: "ServiceAuth",
  environments: {
    prod: {
      envName: "prod",
      centralApi: "https://ppp.hub.deep6.ai/api",
      eventBus: "prod-bus",
      removalPolicy: RemovalPolicy.RETAIN,
    },
    stg: {
      envName: "stg",
      centralApi: "https://ppp.mt-stg.deep6-testing.com/api",
      eventBus: "staging-bus",
      removalPolicy: RemovalPolicy.RETAIN,
    },
    int: {
      envName: "int",
      centralApi: "https://ppp.mt-int.deep6-testing.com/api",
      eventBus: "int-bus",
      removalPolicy: RemovalPolicy.DESTROY,
    },
    poc: {
      envName: "poc",
      centralApi: "https://ppp.mt-poc.deep6-testing.com/api",
      eventBus: "poc-bus",
      removalPolicy: RemovalPolicy.DESTROY,
    },
    eph: {
      envName: "eph",
      centralApi: "https://ppp.{prefix}.deep6.life/api",
      eventBus: "{prefix}-bus",
      removalPolicy: RemovalPolicy.DESTROY,
    },
  },
}
