import {
  Duration,
  Stack,
  aws_iam as iam,
  aws_lambda as lambda,
} from "aws-cdk-lib"
import { Construct } from "constructs"
import { ConfigBuild } from "../config/ConfigBuild"
import { DynamoSingleTable } from "../constructs/DynamoSingleTable"
import { PythonFunctionBase } from "../constructs/PythonFunctionBase"
import { ParameterHelper } from "../helpers/SsmHelper"
import { AppStackProps } from "../interfaces/GenericStackProps"

export class AuthStack extends Stack {
  constructor(scope: Construct, id: string, props: AppStackProps) {
    super(scope, id, props)

    //DDB table creation
    const idpTable = this.createIdpTable(props.appSettings)
    const ssmTable = `/${props.stackName}/idptable/name`.replaceAll("-", "/")
    ParameterHelper.putParameter(this, ssmTable, idpTable.table.tableName)
    props.appSettings.ssmParameters["idpTableSsmKey"] = ssmTable
    //end of DDB table creation

    //lambda layers import
    const layers = this.layersDependencies(props)

    //authorizer function
    const authorizerFn = PythonFunctionBase.defaultFunction(
      this,
      {
        index: "authorizer/",
        layers: layers,
        functionName: "strict-auth",
        timeout: Duration.seconds(10),
        memorySize: 512,
        environment: {
          CENTRAL_API_ENDPOINT: props.appSettings.envVariables.centralApi,
          IDP_TABLE: idpTable.table.tableName,
        },
        bundling: {
          assetExcludes: ["ingestion/*"],
        },
      },
      props.appSettings
    )

    // override the logical Id in the CloudFormation - check if this values is the same for all environments
    const cfnFunction = authorizerFn.node.defaultChild as lambda.CfnFunction
    cfnFunction.overrideLogicalId(
      "StrictAuthorizerStrictAuthorizerHandlerFD98BD7A"
    )

    authorizerFn.addPermission(`${Stack.of(this).stackName}-auth-perm`, {
      principal: new iam.ServicePrincipal("apigateway.amazonaws.com"),
    })

    idpTable.table.grantReadWriteData(authorizerFn)
  }

  // this should not be here. TODO: move to a separate stack
  private createIdpTable(appSettings: ConfigBuild): DynamoSingleTable {
    return new DynamoSingleTable(this, "StudyMembershipOrgTable", {
      tableName: `org-table-${appSettings.stage}`,
      appSettings,
    })
  }

  private layersDependencies(props: AppStackProps): lambda.ILayerVersion[] {
    //lambda layers import
    const pwrTollsARN = `arn:aws:lambda:${this.region}:017000801446:layer:AWSLambdaPowertoolsPythonV2:79`
    const pwrToolsLayer = lambda.LayerVersion.fromLayerVersionArn(
      this,
      "power-tools",
      pwrTollsARN
    )

    const thirdPartyLayerArn = ParameterHelper.getParameterWithAtt(
      this,
      props.appSettings.ssmParameters["thirdPartyLayerSsmKey"]
    )
    const thirdPartyCodeLayer = lambda.LayerVersion.fromLayerVersionAttributes(
      this,
      "third-party-code-layer",
      {
        layerVersionArn: thirdPartyLayerArn,
        compatibleRuntimes: [lambda.Runtime.PYTHON_3_11],
      }
    )
    //end of lambda layers import

    return [pwrToolsLayer, thirdPartyCodeLayer]
  }
}
