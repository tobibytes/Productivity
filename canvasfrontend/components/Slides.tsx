"use client";

import Reveal from 'reveal.js';
import Markdown from 'reveal.js/plugin/markdown/markdown.esm.js';

import 'reveal.js/dist/reveal.css';
// import 'reveal.js/dist/theme/black.css';
import 'reveal.js/dist/theme/moon.css'; // More balanced
import { useEffect, useRef } from 'react';

export default function Slides({ markdownText } : { markdownText: string}) {
  const revealRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (!revealRef.current) return;

    const deck = new Reveal(revealRef.current, {
      embedded: true,
      plugins: [Markdown],
    });

    deck.initialize().then(() => {
      console.log("✅ Reveal initialized");
    });
  }, []);

  return (
    <div className="reveal" ref={revealRef} style={{ height: '60vh', width: '100%' }}>
      <div className="slides">
        <section data-markdown="">
          <textarea
            data-template=""
            readOnly
            defaultValue={markdownText || "## No slides found 😢"}
          />
        </section>
      </div>
    </div>
  );
}