import {
  Checkbox,
  Description,
  Input,
  Label,
  ListBox,
  Radio,
  RadioGroup,
  Select,
  TextArea,
  TextField,
} from "@heroui/react";

import { ShowcaseCard, ShowcaseSection } from "./section";

export function FormsShowcase() {
  return (
    <ShowcaseSection
      description="Inputs, selection controls, and the fields that hold them."
      id="forms"
      title="Forms"
    >
      <ShowcaseCard className="flex flex-col gap-4" title="Text field">
        <TextField className="w-full max-w-64" name="email" type="email">
          <Label>Email</Label>
          <Input placeholder="Enter your email" />
        </TextField>
      </ShowcaseCard>

      <ShowcaseCard className="flex flex-col gap-4" title="Text area">
        <TextArea
          aria-label="Quick project update"
          className="h-24 w-full"
          placeholder="Share a quick project update..."
        />
      </ShowcaseCard>

      <ShowcaseCard title="Checkbox">
        <Checkbox name="terms">
          <Checkbox.Content>
            <Checkbox.Control>
              <Checkbox.Indicator />
            </Checkbox.Control>
            Accept terms and conditions
          </Checkbox.Content>
        </Checkbox>
      </ShowcaseCard>

      <ShowcaseCard className="flex flex-col gap-3" title="Radio group">
        <RadioGroup defaultValue="premium" name="plan">
          <Label>Plan selection</Label>
          <Description>Choose the plan that suits you best</Description>
          <Radio value="basic">
            <Radio.Content>
              <Radio.Control>
                <Radio.Indicator />
              </Radio.Control>
              Basic
            </Radio.Content>
          </Radio>
          <Radio value="premium">
            <Radio.Content>
              <Radio.Control>
                <Radio.Indicator />
              </Radio.Control>
              Premium
            </Radio.Content>
          </Radio>
          <Radio value="business">
            <Radio.Content>
              <Radio.Control>
                <Radio.Indicator />
              </Radio.Control>
              Business
            </Radio.Content>
          </Radio>
        </RadioGroup>
      </ShowcaseCard>

      <ShowcaseCard className="flex flex-col gap-4" title="Select">
        <Select className="w-full max-w-64" placeholder="Select one">
          <Label>State</Label>
          <Select.Trigger>
            <Select.Value />
            <Select.Indicator />
          </Select.Trigger>
          <Select.Popover>
            <ListBox>
              <ListBox.Item id="florida" textValue="Florida">
                Florida
                <ListBox.ItemIndicator />
              </ListBox.Item>
              <ListBox.Item id="delaware" textValue="Delaware">
                Delaware
                <ListBox.ItemIndicator />
              </ListBox.Item>
              <ListBox.Item id="california" textValue="California">
                California
                <ListBox.ItemIndicator />
              </ListBox.Item>
              <ListBox.Item id="texas" textValue="Texas">
                Texas
                <ListBox.ItemIndicator />
              </ListBox.Item>
            </ListBox>
          </Select.Popover>
        </Select>
      </ShowcaseCard>
    </ShowcaseSection>
  );
}
