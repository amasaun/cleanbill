import { Construct } from "constructs"
import { Tags } from "aws-cdk-lib"

type CustomTag = {
  key: string
  value: string
}

export class TagHelper {
  static addTags(customStack: Construct, tags: CustomTag[]) {
    tags.forEach(function (tag) {
      Tags.of(customStack).add(tag.key, tag.value)
    })
  }
}
