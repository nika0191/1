import { ToastProvider } from "@heroui/react";

export function Provider({ children }: { children: React.ReactNode }) {
  return (
    <>
      {children}
      <ToastProvider />
    </>
  );
}
