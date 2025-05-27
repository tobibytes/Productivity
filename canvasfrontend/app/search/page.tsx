'use client';
import React, { useState } from "react";
import SearchResultCard from "@/components/SearchResultCard"; // adjust path as needed

const dummyResults = [
  {
    content: "A 2-input multiplexer selects between two input signals based on a control signal.",
    courseId: "CSC101",
    moduleId: "M01",
    moduleItemId: "Note1",
    text: "multiplexer",
  },
  {
    content: "Verilog allows modeling of digital systems at the behavioral and structural levels.",
    courseId: "CSC101",
    moduleId: "M02",
    moduleItemId: "Note2",
    text: "Verilog",
  },
];


interface SearchData {
  courseId?: string;
  moduleId?: string;
  email: string;
  text: string;
}

const SearchPage = () => {
  const [searchTerm, setSearchTerm] = useState("");
  const [course, setCourse] = useState("");
  const [module, setModule] = useState("");
  const [item, setItem] = useState("");
  const [results, setResults] = useState(dummyResults); // Replace with real results from backend


  async function getCourses(email: string) {
    try {
    
      const response = await fetch(`${process.env.BACKEND_URL}/courses?email=${email}`);
      if (!response.ok) {
        throw new Error("Failed to fetch courses");
      }
      const data = await response.json();
      return data;
    } catch (error) {
      console.error("Error fetching courses:", error);
      return [];
    }
  }
  async function getModules(id: string, email: string) {
    try {
      const response = await fetch(`${process.env.BACKEND_URL}/courses/${id}/modules?email=${email}`);
      if (!response.ok) {
        throw new Error("Failed to fetch modules");
      }
      const data = await response.json();
      return data;
    } catch (error) {
      console.error("Error fetching modules:", error);
      return [];
    }
  }

  async function searchNote(searchData: SearchData) {
    try {
      const response = await fetch(`${process.env.BACKEND_URL}/search`, {
        method: "POST",
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(searchData)
      })
    }
    catch (error) {
      console.error("Error searching notes:", error);
      return [];
    }
  }


  return (
    <div className="max-w-4xl mx-auto px-6 py-12">
      <h1 className="text-3xl font-bold mb-4 text-gray-800">Search</h1>

      <input
        type="text"
        placeholder="Search..."
        value={searchTerm}
        onChange={(e) => setSearchTerm(e.target.value)}
        className="w-full border border-gray-300 rounded px-4 py-2 mb-4 focus:outline-none focus:ring-2 focus:ring-blue-500"
      />

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
        <select
          value={course}
          onChange={(e) => setCourse(e.target.value)}
          className="border border-gray-300 rounded px-4 py-2"
        >
          <option value="">All Courses</option>
          <option value="CSC101">CSC101</option>
        </select>

        <select
          value={module}
          onChange={(e) => setModule(e.target.value)}
          className="border border-gray-300 rounded px-4 py-2"
        >
          <option value="">All Modules</option>
          <option value="M01">Module 1</option>
        </select>
      </div>

      <button
        onClick={() => console.log("Search...")}
        className="bg-blue-600 text-white px-6 py-2 rounded hover:bg-blue-700 transition mb-8"
      >
        Search
      </button>

      <div className="space-y-4">
        {results.length > 0 ? (
          results.map((res, i) => (
            <SearchResultCard key={i} {...res} />
          ))
        ) : (
          <p className="text-gray-500">No results found.</p>
        )}
      </div>
    </div>
  );
};

export default SearchPage;