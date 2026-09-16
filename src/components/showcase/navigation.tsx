"use client";

import { Accordion, Breadcrumbs, Pagination, Tabs } from "@heroui/react";
import { ChevronDown } from "lucide-react";
import { useState } from "react";

import { ShowcaseCard, ShowcaseSection } from "./section";

const accordionItems = [
  {
    content:
      "Browse our products, add items to your cart, and proceed to checkout.",
    title: "How do I place an order?",
  },
  {
    content: "Yes, you can modify or cancel your order before it's shipped.",
    title: "Can I modify or cancel my order?",
  },
  {
    content: "We accept all major credit cards, including Visa and Mastercard.",
    title: "What payment methods do you accept?",
  },
];

function PaginationDemo() {
  const [page, setPage] = useState(1);
  const totalPages = 4;

  return (
    <Pagination className="justify-start">
      <Pagination.Content>
        <Pagination.Item>
          <Pagination.Previous
            isDisabled={page === 1}
            onPress={() => setPage((p) => p - 1)}
          >
            <Pagination.PreviousIcon />
          </Pagination.Previous>
        </Pagination.Item>
        {Array.from({ length: totalPages }, (_, i) => i + 1).map((p) => (
          <Pagination.Item key={p}>
            <Pagination.Link isActive={p === page} onPress={() => setPage(p)}>
              {p}
            </Pagination.Link>
          </Pagination.Item>
        ))}
        <Pagination.Item>
          <Pagination.Next
            isDisabled={page === totalPages}
            onPress={() => setPage((p) => p + 1)}
          >
            <Pagination.NextIcon />
          </Pagination.Next>
        </Pagination.Item>
      </Pagination.Content>
    </Pagination>
  );
}

export function NavigationShowcase() {
  return (
    <ShowcaseSection
      description="Tabs, breadcrumbs, accordions, and pagination for moving through content."
      id="navigation"
      title="Navigation"
    >
      <ShowcaseCard className="flex flex-col gap-4" title="Tabs">
        <Tabs className="w-full">
          <Tabs.ListContainer>
            <Tabs.List aria-label="Options">
              <Tabs.Tab id="overview">
                Overview
                <Tabs.Indicator />
              </Tabs.Tab>
              <Tabs.Tab id="analytics">
                Analytics
                <Tabs.Indicator />
              </Tabs.Tab>
              <Tabs.Tab id="reports">
                Reports
                <Tabs.Indicator />
              </Tabs.Tab>
            </Tabs.List>
          </Tabs.ListContainer>
          <Tabs.Panel className="pt-4 text-sm text-muted" id="overview">
            View your project overview and recent activity.
          </Tabs.Panel>
          <Tabs.Panel className="pt-4 text-sm text-muted" id="analytics">
            Track your metrics and analyze performance data.
          </Tabs.Panel>
          <Tabs.Panel className="pt-4 text-sm text-muted" id="reports">
            Generate and download detailed reports.
          </Tabs.Panel>
        </Tabs>
      </ShowcaseCard>

      <ShowcaseCard title="Breadcrumbs">
        <Breadcrumbs>
          <Breadcrumbs.Item href="#">Home</Breadcrumbs.Item>
          <Breadcrumbs.Item href="#">Products</Breadcrumbs.Item>
          <Breadcrumbs.Item href="#">Electronics</Breadcrumbs.Item>
          <Breadcrumbs.Item>Laptop</Breadcrumbs.Item>
        </Breadcrumbs>
      </ShowcaseCard>

      <ShowcaseCard className="flex flex-col gap-4" title="Accordion">
        <Accordion className="w-full">
          {accordionItems.map((item, index) => (
            <Accordion.Item key={index}>
              <Accordion.Heading>
                <Accordion.Trigger>
                  {item.title}
                  <Accordion.Indicator>
                    <ChevronDown />
                  </Accordion.Indicator>
                </Accordion.Trigger>
              </Accordion.Heading>
              <Accordion.Panel>
                <Accordion.Body className="text-sm text-muted">
                  {item.content}
                </Accordion.Body>
              </Accordion.Panel>
            </Accordion.Item>
          ))}
        </Accordion>
      </ShowcaseCard>

      <ShowcaseCard title="Pagination">
        <PaginationDemo />
      </ShowcaseCard>
    </ShowcaseSection>
  );
}
