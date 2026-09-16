"use client";

import {
  Button,
  Dropdown,
  Label,
  Modal,
  Popover,
  Tooltip,
} from "@heroui/react";
import { CircleAlert, Rocket } from "lucide-react";

import { ShowcaseCard, ShowcaseSection } from "./section";

export function OverlaysShowcase() {
  return (
    <ShowcaseSection
      description="Modals, popovers, tooltips, and menus layered above the page."
      id="overlays"
      title="Overlays"
    >
      <ShowcaseCard title="Modal">
        <Modal>
          <Button variant="secondary">Open Modal</Button>
          <Modal.Backdrop>
            <Modal.Container>
              <Modal.Dialog className="sm:max-w-[360px]">
                <Modal.CloseTrigger />
                <Modal.Header>
                  <Modal.Icon className="bg-default text-foreground">
                    <Rocket className="size-5" />
                  </Modal.Icon>
                  <Modal.Heading>Welcome to HeroUI</Modal.Heading>
                </Modal.Header>
                <Modal.Body>
                  <p className="text-sm text-muted">
                    A beautiful, fast, and modern React UI library for building
                    accessible web applications.
                  </p>
                </Modal.Body>
                <Modal.Footer>
                  <Button className="w-full" slot="close">
                    Continue
                  </Button>
                </Modal.Footer>
              </Modal.Dialog>
            </Modal.Container>
          </Modal.Backdrop>
        </Modal>
      </ShowcaseCard>

      <ShowcaseCard title="Popover">
        <Popover>
          <Button variant="secondary">Click me</Button>
          <Popover.Content className="max-w-64">
            <Popover.Dialog>
              <Popover.Heading>Popover Title</Popover.Heading>
              <p className="mt-2 text-sm text-muted">
                This is the popover content. You can put any content here.
              </p>
            </Popover.Dialog>
          </Popover.Content>
        </Popover>
      </ShowcaseCard>

      <ShowcaseCard title="Tooltip">
        <Tooltip delay={0}>
          <Button variant="secondary">Hover me</Button>
          <Tooltip.Content>
            <p>This is a tooltip</p>
          </Tooltip.Content>
        </Tooltip>
        <Tooltip delay={0}>
          <Button isIconOnly aria-label="More information" variant="tertiary">
            <CircleAlert className="size-4" />
          </Button>
          <Tooltip.Content>
            <p>More information</p>
          </Tooltip.Content>
        </Tooltip>
      </ShowcaseCard>

      <ShowcaseCard title="Dropdown menu">
        <Dropdown>
          <Button aria-label="Menu" variant="secondary">
            Actions
          </Button>
          <Dropdown.Popover>
            <Dropdown.Menu onAction={(key) => console.log(`Selected: ${key}`)}>
              <Dropdown.Item id="new-file" textValue="New file">
                <Label>New file</Label>
              </Dropdown.Item>
              <Dropdown.Item id="copy-link" textValue="Copy link">
                <Label>Copy link</Label>
              </Dropdown.Item>
              <Dropdown.Item id="edit-file" textValue="Edit file">
                <Label>Edit file</Label>
              </Dropdown.Item>
              <Dropdown.Item
                id="delete-file"
                textValue="Delete file"
                variant="danger"
              >
                <Label>Delete file</Label>
              </Dropdown.Item>
            </Dropdown.Menu>
          </Dropdown.Popover>
        </Dropdown>
      </ShowcaseCard>
    </ShowcaseSection>
  );
}
