import React from "react";

interface SearchResultCardProps {
  content: string;
  courseId?: string;
  moduleId?: string;
  moduleItemId?: string;
  text?: string;
}

const highlightMatch = (content: string, query: string): string => {
  if (!query) return content;

  const escapedQuery = query.replace(/[.*+?^${}()|[\]\\]/g, "\\$&"); // Escape regex characters
  const regex = new RegExp(`(${escapedQuery})`, "gi");

  return content.replace(regex, '<mark class="bg-yellow-200 font-semibold">$1</mark>');
};

const SearchResultCard: React.FC<SearchResultCardProps> = ({
  content,
  courseId,
  moduleId,
  moduleItemId,
  text
}) => {
  const highlightedContent = highlightMatch(content, text || "");

  return (
    <div className="bg-white rounded-xl shadow-md p-4 space-y-2 border hover:shadow-lg transition">
      <div
        className="text-gray-800 text-sm whitespace-pre-line"
        dangerouslySetInnerHTML={{ __html: highlightedContent }}
      />
      <div className="text-xs text-gray-500 flex justify-between pt-2 border-t">
        <span>Course: {courseId || "—"}</span>
        <span>Module: {moduleId || "—"}</span>
        <span>Item: {moduleItemId || "—"}</span>
      </div>
    </div>
  );
};

export default SearchResultCard;