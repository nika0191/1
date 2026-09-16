import { Avatar, Badge, Card, Chip, Link } from "@heroui/react";
import { CircleDollarSign } from "lucide-react";

import { ShowcaseCard, ShowcaseSection } from "./section";

const GREEN_AVATAR_URL =
  "https://heroui-assets.nyc3.cdn.digitaloceanspaces.com/avatars/green.jpg";
const BLUE_AVATAR_URL =
  "https://heroui-assets.nyc3.cdn.digitaloceanspaces.com/avatars/blue.jpg";

export function DataDisplayShowcase() {
  return (
    <ShowcaseSection
      description="Avatars, badges, tags, and cards for presenting content."
      id="data-display"
      title="Data Display"
    >
      <ShowcaseCard title="Avatar">
        <Avatar>
          <Avatar.Image alt="Jane Doe" src={GREEN_AVATAR_URL} />
          <Avatar.Fallback>JD</Avatar.Fallback>
        </Avatar>
        <Avatar>
          <Avatar.Image alt="Blue" src={BLUE_AVATAR_URL} />
          <Avatar.Fallback>B</Avatar.Fallback>
        </Avatar>
        <Avatar>
          <Avatar.Fallback>JR</Avatar.Fallback>
        </Avatar>
      </ShowcaseCard>

      <ShowcaseCard title="Badge">
        <Badge.Anchor>
          <Avatar>
            <Avatar.Image alt="Jane" src={GREEN_AVATAR_URL} />
            <Avatar.Fallback>JD</Avatar.Fallback>
          </Avatar>
          <Badge color="danger" size="sm">
            5
          </Badge>
        </Badge.Anchor>
        <Badge.Anchor>
          <Avatar>
            <Avatar.Image alt="Blue" src={BLUE_AVATAR_URL} />
            <Avatar.Fallback>B</Avatar.Fallback>
          </Avatar>
          <Badge color="success" placement="bottom-right" size="sm" />
        </Badge.Anchor>
      </ShowcaseCard>

      <ShowcaseCard title="Chip">
        <Chip>Default</Chip>
        <Chip color="accent">Accent</Chip>
        <Chip color="success">Success</Chip>
        <Chip color="warning">Warning</Chip>
        <Chip color="danger">Danger</Chip>
      </ShowcaseCard>

      <ShowcaseCard title="Card">
        <Card className="w-full">
          <CircleDollarSign
            aria-label="Dollar sign icon"
            className="size-6 text-primary"
            role="img"
          />
          <Card.Header>
            <Card.Title>Become an Acme Creator!</Card.Title>
            <Card.Description>
              Sign up today and start earning credits from your fans and
              followers.
            </Card.Description>
          </Card.Header>
          <Card.Footer>
            <Link
              aria-label="Go to Acme Creator Hub (opens in new tab)"
              href="https://heroui.com"
              rel="noopener noreferrer"
              target="_blank"
            >
              Creator Hub
              <Link.Icon aria-hidden="true" />
            </Link>
          </Card.Footer>
        </Card>
      </ShowcaseCard>
    </ShowcaseSection>
  );
}
