"use client";

import { useEffect, useState } from "react";

export interface FlashcardProps {
  question: string;
  answer: string;
}

const pastelColors = [
  "bg-red-100",
  "bg-orange-100",
  "bg-yellow-100",
  "bg-green-100",
  "bg-teal-100",
  "bg-blue-100",
  "bg-indigo-100",
  "bg-purple-100",
  "bg-pink-100",
];

export default function Flashcard({ question, answer }: FlashcardProps) {
  const [flipped, setFlipped] = useState(false);
  const [bgColor, setBgColor] = useState("bg-white");

  useEffect(() => {
    const random = Math.floor(Math.random() * pastelColors.length);
    setBgColor(pastelColors[random]);
  }, []);

  return (
    <div
      className={`relative w-full max-w-sm h-64 rounded-2xl shadow-lg transition-transform duration-500 cursor-pointer transform-gpu perspective`}
      onClick={() => setFlipped(!flipped)}
    >
      <div
        className={`absolute inset-0 transition-transform duration-500 transform ${
          flipped ? "rotate-y-180" : ""
        }`}
        style={{ transformStyle: "preserve-3d" }}
      >
        {/* Front */}
        <div
          className={`absolute inset-0 ${bgColor} flex flex-col justify-center items-center p-6 text-center backface-hidden rounded-2xl`}
        >
          <h3 className="text-lg font-semibold text-gray-800">
            {question}
          </h3>
          <p className="text-sm text-gray-500 mt-2">Click to reveal answer</p>
        </div>

        {/* Back */}
        <div className="absolute inset-0 bg-white text-gray-900 flex flex-col justify-center items-center p-6 rounded-2xl rotate-y-180 backface-hidden">
          <h4 className="text-md font-medium mb-2 text-center">Answer</h4>
          <p className="text-sm text-center leading-relaxed">{answer}</p>
          <p className="text-xs text-gray-400 mt-4">Click to flip back</p>
        </div>
      </div>
    </div>
  );
}