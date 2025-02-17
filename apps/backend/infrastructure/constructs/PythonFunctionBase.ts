import {
  PythonFunction,
  PythonFunctionProps,
} from "@aws-cdk/aws-lambda-python-alpha"
import {
  Duration,
  aws_iam as iam,
  aws_lambda as lambda,
  aws_logs as logs,
  Stack,
} from "aws-cdk-lib"
import { Construct } from "constructs"
import { ConfigBuild, StackStage } from "../config/ConfigBuild"

export abstract class PythonFunctionBase {
  static defaultFunction(
    scope: Construct,
    functionProps: Partial<PythonFunctionProps>,
    appSettings: ConfigBuild
  ) {
    const fnName = `${Stack.of(scope).stackName}-${
      functionProps.functionName
    }`.toLowerCase()

    // log group definitions
    const logGroup = new logs.LogGroup(scope, `${fnName}-log-group`, {
      logGroupName: `/aws/lambda/${fnName}-log-group`,
      removalPolicy: appSettings.removalPolicy,
      retention:
        appSettings.stage !== StackStage.PRODUCTION
          ? logs.RetentionDays.ONE_WEEK
          : logs.RetentionDays.THREE_MONTHS,
    })

    const exclude = [".venv", "tests/*", "test/*", "scripts/*", "layers/*"]

    const defaultProps: PythonFunctionProps = {
      runtime: lambda.Runtime.PYTHON_3_11,
      timeout: functionProps.timeout ?? Duration.seconds(15),
      memorySize: 512,
      ...functionProps,
      bundling: {
        assetExcludes: exclude.concat(
          functionProps.bundling?.assetExcludes ?? []
        ),
      },
      index: `src/${functionProps.index}index.py`,
      functionName: fnName,
      entry: "app/",
      logGroup: logGroup,
      tracing: lambda.Tracing.ACTIVE,
      environment: {
        LOG_LEVEL: "INFO",
        POWERTOOLS_SERVICE_NAME: fnName,
        ...functionProps.environment,
      },
    }

    const fn = new PythonFunction(scope, fnName, defaultProps)

    if (!fn.role) {
      throw new Error(`Function ${fnName} has no role`)
    }

    fn.role.addManagedPolicy(
      iam.ManagedPolicy.fromAwsManagedPolicyName("AWSXRayDaemonWriteAccess")
    )

    return fn
  }
}
