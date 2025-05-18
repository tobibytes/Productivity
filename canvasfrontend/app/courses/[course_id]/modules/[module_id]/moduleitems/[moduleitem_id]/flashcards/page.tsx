import Flashcard from "@/components/Flashcard";
import { useEffect, useState } from "react";

const flashcards = [
  {
    question: "What is active recall?",
    answer:
      "A learning technique where you try to remember information without looking at the source, strengthening memory connections.",
  },
  {
    question: "What does dual coding theory suggest?",
    answer:
      "That combining visual and verbal information enhances learning and memory retention.",
  },
  {
    question: "Why use spaced repetition?",
    answer:
      "It helps retain information longer by reviewing just before you're likely to forget.",
  },
  {
    question: "What's a good flashcard layout?",
    answer:
      "Use a single question on the front, and a focused, concise answer on the back with spacing and emphasis on key terms.",
  },
  {
    question: "How do visuals help flashcards?",
    answer:
      "They activate dual channels in the brain, improving memory encoding and recall speed.",
  },
];
const [flashcard, setFlashcard] = useState(flashcards);

export default function FlashcardsPage() {
  return (
    <div className="w-full px-6 py-10">
      <h1 className="text-3xl font-bold text-center text-gray-800 mb-8">
        Flashcards
      </h1>

      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-8 place-items-center">
        {flashcards.map((card, index) => (
          <Flashcard key={index} {...card} />
        ))}
      </div>
    </div>
  );
}