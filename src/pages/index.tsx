import { GithubIcon } from "@/components/icons";
import { subtitle, title } from "@/components/primitives";
import DefaultLayout from "@/layouts/default";

export default function IndexPage() {
  return (
    <DefaultLayout>
      <section className="flex flex-col items-center justify-center gap-4 py-8 md:py-10">
        <div className="inline-block max-w-lg text-center justify-center">
          <span className={title()}>Make&nbsp;</span>
          <span className={title({ color: "blue" })}>beautiful&nbsp;</span>
          <br />
          <span className={title()}>interfaces with HeroUI components.</span>
          <div className={subtitle({ class: "mt-4" })}>
            Beautiful, fast and modern React UI library, built on Tailwind CSS
            v4 and React Aria.
          </div>
        </div>

        <div className="flex gap-3">
          <a
            className="button button--primary button--md rounded-full"
            href="/components"
          >
            Browse Components
          </a>
          <a
            className="button button--tertiary button--md rounded-full"
            href="https://github.com/heroui-inc/heroui"
            rel="noopener noreferrer"
            target="_blank"
          >
            <GithubIcon size={20} />
            GitHub
          </a>
        </div>

        <div className="mt-8">
          <div className="flex items-center gap-2 rounded-xl bg-surface shadow-surface px-4 py-2">
            <pre className="text-sm font-medium font-mono">
              Explore every category on the{" "}
              <code className="px-2 py-1 h-fit font-mono font-normal inline whitespace-nowrap rounded-sm bg-accent/20 text-accent text-sm">
                /components
              </code>{" "}
              page
            </pre>
          </div>
        </div>
      </section>
    </DefaultLayout>
  );
}
