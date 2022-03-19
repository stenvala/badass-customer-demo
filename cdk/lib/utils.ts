import { CdkProps } from "./props";

export function getResourceSuffix(props: CdkProps): string {
  return `-${props.env.region}-${props.env.stage}${props.stackSuffix}`;
}
