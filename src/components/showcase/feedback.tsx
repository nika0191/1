"use client";

import {
  Alert,
  Button,
  CloseButton,
  Label,
  ProgressBar,
  Skeleton,
  Spinner,
  Switch,
  toast,
} from "@heroui/react";

import { ShowcaseCard, ShowcaseSection } from "./section";

export function FeedbackShowcase() {
  return (
    <ShowcaseSection
      description="Switches, progress, loading states, and messages that keep people informed."
      id="feedback"
      title="Controls & Feedback"
    >
      <ShowcaseCard title="Switch">
        <Switch>
          <Switch.Content>
            <Switch.Control>
              <Switch.Thumb />
            </Switch.Control>
            Enable notifications
          </Switch.Content>
        </Switch>
      </ShowcaseCard>

      <ShowcaseCard className="flex flex-col gap-4" title="Progress bar">
        <ProgressBar aria-label="Loading" className="w-full" value={60}>
          <Label>Loading</Label>
          <ProgressBar.Output />
          <ProgressBar.Track>
            <ProgressBar.Fill />
          </ProgressBar.Track>
        </ProgressBar>
      </ShowcaseCard>

      <ShowcaseCard title="Spinner & skeleton">
        <Spinner />
        <div className="flex-1 space-y-2">
          <Skeleton className="h-3 w-3/5 rounded-lg" />
          <Skeleton className="h-3 w-4/5 rounded-lg" />
        </div>
      </ShowcaseCard>

      <ShowcaseCard title="Toast">
        <Button
          size="sm"
          variant="secondary"
          onPress={() => toast.success("Operation completed")}
        >
          Success
        </Button>
        <Button
          size="sm"
          variant="secondary"
          onPress={() => toast.warning("Please check your settings")}
        >
          Warning
        </Button>
        <Button
          size="sm"
          variant="secondary"
          onPress={() => toast.danger("Something went wrong")}
        >
          Error
        </Button>
      </ShowcaseCard>

      <ShowcaseCard className="flex flex-col gap-3 sm:col-span-2" title="Alert">
        <Alert>
          <Alert.Indicator />
          <Alert.Content>
            <Alert.Title>New features available</Alert.Title>
            <Alert.Description>
              Check out our latest updates including dark mode support and
              improved accessibility.
            </Alert.Description>
          </Alert.Content>
        </Alert>
        <Alert status="danger">
          <Alert.Indicator />
          <Alert.Content>
            <Alert.Title>Unable to connect to server</Alert.Title>
            <Alert.Description>
              We&apos;re experiencing connection issues. Please try again.
            </Alert.Description>
          </Alert.Content>
        </Alert>
        <Alert status="success">
          <Alert.Indicator />
          <Alert.Content>
            <Alert.Title>Profile updated successfully</Alert.Title>
          </Alert.Content>
          <CloseButton />
        </Alert>
      </ShowcaseCard>
    </ShowcaseSection>
  );
}
