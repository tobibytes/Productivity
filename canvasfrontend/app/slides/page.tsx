"use client";

import dynamic from "next/dynamic";

// Dynamically import Reveal Slides client-side only
const Slides = dynamic(() => import("@/components/Slides"), { ssr: false });

export default function SlidesPage() {
  return <Slides markdownText="Hello"/>;
}