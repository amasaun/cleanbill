import { aws_secretsmanager as secret, aws_ssm as ssm } from "aws-cdk-lib"
import { Construct } from "constructs"

import { v4 as uuidv4 } from "uuid"

export abstract class ParameterHelper {
  static getParameter(scope: Construct, name: string, id = "") {
    if (id === "") id = name.replaceAll("/", "-")
    return ssm.StringParameter.fromStringParameterName(scope, id, name)
      .stringValue
  }

  static getParameterWithAtt(scope: Construct, name: string) {
    const id = `id-${uuidv4().substring(0, 10)}`
    return ssm.StringParameter.fromStringParameterAttributes(scope, id, {
      parameterName: name,
    }).stringValue
  }

  static getListParameter(scope: Construct, name: string, id = "") {
    if (id === "") id = name.replaceAll("/", "")
    return ssm.StringListParameter.fromStringListParameterName(scope, id, name)
      .stringListValue
  }

  static lookupParameter(scope: Construct, name: string) {
    return ssm.StringParameter.valueFromLookup(scope, name)
  }

  static valueForParameter(scope: Construct, name: string) {
    return ssm.StringParameter.valueForStringParameter(scope, name)
  }

  static putParameter(
    scope: Construct,
    name: string,
    value: string | string[]
  ) {
    if (typeof value === "string")
      new ssm.StringParameter(scope, name.replaceAll("/", "-"), {
        stringValue: value,
        parameterName: name,
      })
    else
      new ssm.StringListParameter(scope, name.replaceAll("/", "-"), {
        stringListValue: value,
        parameterName: name,
      })
  }

  static createSecret(scope: Construct, name: string) {
    new secret.Secret(scope, name.replaceAll("/", "-"), {
      secretName: name,
    })
  }
}
