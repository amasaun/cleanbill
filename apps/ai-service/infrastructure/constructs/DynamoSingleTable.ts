import { Stack } from "aws-cdk-lib"
import {
  AttributeType,
  BillingMode,
  StreamViewType,
  Table,
} from "aws-cdk-lib/aws-dynamodb"

import { Construct } from "constructs"
import { ConfigBuild, StackStage } from "../config/ConfigBuild"

export interface DynamoSingleTableProps {
  /**
   * Simple Name of the table. Will be appended to Stack Name.
   */
  tableName: string
  /**
   * Enables DynamoDB Streams on the table.
   */
  stream?: StreamViewType
  /**
   * Stage the table is deployed to. This determines if PITR is enabled.
   */
  appSettings: ConfigBuild
}

export class DynamoSingleTable extends Construct {
  public table: Table

  constructor(scope: Construct, id: string, props: DynamoSingleTableProps) {
    super(scope, id)
    const stackName = Stack.of(this).stackName
    this.table = new Table(this, `${stackName}-${props.tableName}`, {
      tableName: `${stackName}-${props.tableName}`,
      billingMode: BillingMode.PAY_PER_REQUEST,
      removalPolicy: props.appSettings.removalPolicy,
      deletionProtection: props.appSettings.stage === StackStage.PRODUCTION,
      partitionKey: { name: "pk", type: AttributeType.STRING },
      sortKey: { name: "sk", type: AttributeType.STRING },
      stream: props.stream,
      pointInTimeRecovery: this.enablePITR(props.appSettings.stage),
    })
  }

  enablePITR(stage: StackStage) {
    return stage === "prod"
  }
}
