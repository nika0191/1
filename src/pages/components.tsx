import { ButtonsShowcase } from "@/components/showcase/buttons";
import { DataDisplayShowcase } from "@/components/showcase/data-display";
import { FeedbackShowcase } from "@/components/showcase/feedback";
import { FormsShowcase } from "@/components/showcase/forms";
import { NavigationShowcase } from "@/components/showcase/navigation";
import { OverlaysShowcase } from "@/components/showcase/overlays";
import DefaultLayout from "@/layouts/default";

const categories = [
  { id: "buttons", label: "Buttons" },
  { id: "forms", label: "Forms" },
  { id: "feedback", label: "Controls & Feedback" },
  { id: "data-display", label: "Data Display" },
  { id: "navigation", label: "Navigation" },
  { id: "overlays", label: "Overlays" },
];

export default function ComponentsPage() {
  return (
    <DefaultLayout>
      <div className="py-8 md:py-10">
        <h1 className="text-3xl font-bold text-foreground md:text-4xl">
          Component Showcase
        </h1>
        <p className="mt-2 max-w-2xl text-muted">
          A tour of HeroUI React components, grouped the same way as the{" "}
          <a
            className="text-accent underline"
            href="https://heroui.com/en/docs/react/components"
            rel="noopener noreferrer"
            target="_blank"
          >
            official component catalog
          </a>
          .
        </p>

        <nav
          aria-label="Component categories"
          className="mt-6 flex flex-wrap gap-2"
        >
          {categories.map((category) => (
            <a
              key={category.id}
              className="rounded-full border border-separator px-3 py-1.5 text-sm text-foreground transition-colors hover:border-accent hover:text-accent"
              href={`#${category.id}`}
            >
              {category.label}
            </a>
          ))}
        </nav>
      </div>

      <ButtonsShowcase />
      <FormsShowcase />
      <FeedbackShowcase />
      <DataDisplayShowcase />
      <NavigationShowcase />
      <OverlaysShowcase />
    </DefaultLayout>
  );
}
