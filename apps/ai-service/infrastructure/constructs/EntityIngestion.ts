import { Duration, RemovalPolicy, Stack, StackProps } from "aws-cdk-lib"
import { EventBus, Rule } from "aws-cdk-lib/aws-events"
import { SqsQueue } from "aws-cdk-lib/aws-events-targets"
import {
  Effect,
  Policy,
  PolicyStatement,
  ServicePrincipal,
} from "aws-cdk-lib/aws-iam"
import { Key } from "aws-cdk-lib/aws-kms"
import { IFunction } from "aws-cdk-lib/aws-lambda"
import { SqsEventSource } from "aws-cdk-lib/aws-lambda-event-sources"
import { Queue, QueueEncryption } from "aws-cdk-lib/aws-sqs"
import { Construct } from "constructs"
import { capitalize } from "../helpers/StringHelpers"

interface EntityIngestionProps extends StackProps {
  /**
   * Id or Entity used for Construct ID
   */
  entity: string
  /**
   * List of external Services, this should listen to events from.
   */
  source: string[]
  /**
   * Name of Entity/DetailType emitted from another service we should be
   * listening too.
   */
  detailType: string[]
  /**
   * Indicates whether the Queue & DLQ should be encrypted. If set to `true` AWS
   * managed KMS is used.
   *
   * @default - false
   */
  encryption?: boolean
  /**
   * Translates to the Queue's maxReceivedCount:
   * The number of times a message can be unsuccesfully dequeued before being
   * moved to the dead-letter queue.
   *
   * @default - 3
   */
  retryCount?: number
  /**
   * Event bus to listen on
   *
   * @default - default
   */
  eventBus?: string
  /**
   * Lambda that will consume form the queue
   */
  handler: IFunction
}

export class EntityIngestion extends Construct {
  readonly defaultRetryCount = 3
  public readonly entity: string
  public readonly eventRule: Rule
  public readonly handler: IFunction
  public readonly ingestionDlq: Queue
  public readonly ingestionQueue: Queue
  public readonly kmsPolicy?: Policy
  public readonly kmsKey?: Key

  constructor(scope: Construct, id: string, props: EntityIngestionProps) {
    super(scope, id)
    this.entity = props.entity
    const encryptionType = props.encryption
      ? QueueEncryption.KMS
      : QueueEncryption.UNENCRYPTED

    this.kmsKey = props.encryption
      ? new Key(this, `Ing${props.entity}Key`, {
          enableKeyRotation: true,
          removalPolicy: RemovalPolicy.DESTROY,
        })
      : undefined

    const stackName = Stack.of(this).stackName

    this.ingestionDlq = new Queue(this, `${capitalize(this.entity)}DLQ`, {
      retentionPeriod: Duration.days(14),
      queueName: `${stackName}-ing-${props.entity.toLowerCase()}-DLQ`,
      encryption: encryptionType,
      encryptionMasterKey: this.kmsKey,
    })

    this.ingestionQueue = new Queue(this, `${capitalize(this.entity)}Queue`, {
      queueName: `${stackName}-ing-${props.entity.toLowerCase()}`,
      deadLetterQueue: {
        queue: this.ingestionDlq,
        maxReceiveCount: props.retryCount
          ? props.retryCount
          : this.defaultRetryCount,
      },
      visibilityTimeout: Duration.seconds(15),
      encryption: encryptionType,
      encryptionMasterKey: this.kmsKey,
    })

    this.handler = props.handler
    this.handler.addEventSource(
      new SqsEventSource(this.ingestionQueue, {
        batchSize: 10,
        reportBatchItemFailures: true,
      })
    )

    this.eventRule = new Rule(this, `Ingest${capitalize(this.entity)}Event`, {
      ruleName: `${
        Stack.of(this).stackName
      }-ing-${this.entity.toLowerCase()}-event`,
      eventPattern: {
        source: props.source,
        detailType: props.detailType,
      },
      eventBus: props.eventBus
        ? EventBus.fromEventBusName(this, "TheEventBus", props.eventBus)
        : EventBus.fromEventBusName(this, "TheEventBus", "default"),
      targets: [new SqsQueue(this.ingestionQueue)],
    })

    if (props.encryption) {
      const kmsStatement = new PolicyStatement({
        actions: ["kms:GenerateDataKey", "kms:Decrypt"],
        effect: Effect.ALLOW,
        resources: ["*"],
      })
      this.kmsPolicy = new Policy(this, `${this.entity}-KmsPolicy`, {
        statements: [kmsStatement],
      })
      this.handler.role?.attachInlinePolicy(this.kmsPolicy)

      const eventsPrincipal = new ServicePrincipal("events.amazonaws.com")
      this.kmsKey?.grantEncryptDecrypt(eventsPrincipal)
      this.ingestionQueue.grantSendMessages(eventsPrincipal)
      this.ingestionDlq.grantSendMessages(eventsPrincipal)
    }
  }
}
