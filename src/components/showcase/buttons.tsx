import { Button } from "@heroui/react";
import { Globe, Mail, Plus, Trash2 } from "lucide-react";

import { ShowcaseCard, ShowcaseSection } from "./section";

export function ButtonsShowcase() {
  return (
    <ShowcaseSection
      description="Actions people can press, in every visual weight."
      id="buttons"
      title="Buttons"
    >
      <ShowcaseCard title="Variants">
        <Button>Primary</Button>
        <Button variant="secondary">Secondary</Button>
        <Button variant="tertiary">Tertiary</Button>
        <Button variant="outline">Outline</Button>
        <Button variant="ghost">Ghost</Button>
        <Button variant="danger">Danger</Button>
        <Button variant="danger-soft">Danger Soft</Button>
      </ShowcaseCard>
      <ShowcaseCard title="With icons">
        <Button>
          <Globe className="size-4" />
          Search
        </Button>
        <Button variant="secondary">
          <Plus className="size-4" />
          Add Member
        </Button>
        <Button variant="tertiary">
          <Mail className="size-4" />
          Email
        </Button>
        <Button variant="danger">
          <Trash2 className="size-4" />
          Delete
        </Button>
      </ShowcaseCard>
      <ShowcaseCard title="Sizes">
        <Button size="sm">Small</Button>
        <Button size="md">Medium</Button>
        <Button size="lg">Large</Button>
      </ShowcaseCard>
      <ShowcaseCard title="States">
        <Button isDisabled>Disabled</Button>
        <Button isPending>Pending</Button>
        <Button isIconOnly aria-label="Add" variant="secondary">
          <Plus className="size-4" />
        </Button>
      </ShowcaseCard>
    </ShowcaseSection>
  );
}
