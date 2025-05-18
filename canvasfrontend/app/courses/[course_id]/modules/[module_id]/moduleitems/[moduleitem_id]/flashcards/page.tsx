import Flashcard, { FlashcardProps } from "@/components/Flashcard";
import { useParams } from "next/navigation";
import { useEffect, useState } from "react";

export default function FlashcardsPage() {
  const {moduleitem_id} = useParams();
  const [flashcards, setFlashcards] = useState<FlashcardProps[]>([]);

  useEffect(() => {
    const email = sessionStorage.getItem("email");
    async function fetchFlashcards() {
      const response = await fetch(`${process.env.BACKEND_URL}/moduleitems/${moduleitem_id}/flashcards?email=${email}`);
      const data = await response.json();
      setFlashcards(data.flashcards);
    }
    fetchFlashcards();
  },[]);

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