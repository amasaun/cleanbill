import { Stack, aws_lambda as lambda } from "aws-cdk-lib"
import { Construct } from "constructs"
import { ParameterHelper } from "../helpers/SsmHelper"
import { AppStackProps } from "../interfaces/GenericStackProps"

import { PythonLayerVersion } from "@aws-cdk/aws-lambda-python-alpha"
import { camelCase, kebabCase, snakeCase } from "lodash"
import * as path from "path"

export class LayerStack extends Stack {
  readonly authLambdaLayer: lambda.LayerVersion

  constructor(scope: Construct, id: string, props: AppStackProps) {
    super(scope, id, props)

    this.authLambdaLayer = this.buildLayer(props, "third-party")
  }

  private buildLayer(props: AppStackProps, folderName: string) {
    const pathLayer = path.join(
      __dirname,
      "../../app/layers/".concat(`${snakeCase(folderName)}/`)
    )

    const layerVersionName = kebabCase(`${props.stackName}-${folderName}`)

    const layer = new PythonLayerVersion(this, layerVersionName, {
      description:
        `this is a layer for service ${props.appSettings.serviceName}`.toLowerCase(),
      layerVersionName,
      compatibleRuntimes: [lambda.Runtime.PYTHON_3_11],
      compatibleArchitectures: [lambda.Architecture.X86_64],
      entry: pathLayer,
      removalPolicy: props.appSettings.removalPolicy,
    })

    const ssmKey = `/${layerVersionName}/layer/version/arn`
    ParameterHelper.putParameter(this, ssmKey, layer.layerVersionArn)
    props.appSettings.ssmParameters[camelCase(`${folderName}LayerSsmKey`)] =
      ssmKey

    return layer
  }
}
