import { Stack, aws_dynamodb as ddb, aws_lambda as lambda } from "aws-cdk-lib"
import { Construct } from "constructs"
import { AppStackProps } from "../interfaces/GenericStackProps"
import { ParameterHelper } from "../helpers/SsmHelper"
import { PythonFunctionBase } from "../constructs/PythonFunctionBase"
import { EntityIngestion } from "../constructs/EntityIngestion"

export class IngestionStack extends Stack {
  constructor(scope: Construct, id: string, props: AppStackProps) {
    super(scope, id, props)

    // importing layers dependencies
    const layers = this.layersDependencies(props)

    // importing data table dependencies
    const idpTable = this.ddbTableDependencies(props, "idpTableSsmKey")

    //ingestion function
    const ingestionFunction = PythonFunctionBase.defaultFunction(
      this,
      {
        index: "ingestion/",
        layers: layers,
        functionName: "organization-ingestion",
        memorySize: 512,
        environment: {
          CENTRAL_API_ENDPOINT: props.appSettings.envVariables.centralApi,
          IDP_TABLE: idpTable.tableName,
        },
        bundling: {
          assetExcludes: ["authorizer/*"],
        },
      },
      props.appSettings
    )

    idpTable.grantReadWriteData(ingestionFunction)
    //end of authorizer function

    new EntityIngestion(this, "OrganizationIdpIngestion", {
      detailType: ["HealthSystemOrganization", "SponsorOrganization"],
      encryption: true,
      eventBus: props.appSettings.envVariables.eventBus,
      entity: "Organization",
      handler: ingestionFunction,
      retryCount: 1,
      source: ["organization-api", "eng-833-script"],
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

  private ddbTableDependencies(
    props: AppStackProps,
    ssmTableParameterKey: string
  ): ddb.ITable {
    const tableName = ParameterHelper.getParameterWithAtt(
      this,
      props.appSettings.ssmParameters[ssmTableParameterKey]
    )

    return ddb.Table.fromTableName(this, ssmTableParameterKey, tableName)
  }
}
