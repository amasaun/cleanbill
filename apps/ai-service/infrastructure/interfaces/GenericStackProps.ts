import { StackProps } from "aws-cdk-lib"
import { ConfigBuild } from "../config/ConfigBuild"

export interface AppStackProps extends StackProps {
  appSettings: ConfigBuild
}
