"use client";

import { useParams, useSearchParams } from "next/navigation";
import { useEffect, useState } from "react";

const CoursePage = () => {
  const { course_id } = useParams();
  const searchParams = useSearchParams();

  const [course, setCourse] = useState<any | null>(null);


  const [email, setEmail] = useState<string | null>(null);

  useEffect(() => {
    const emailFromStorage = sessionStorage.getItem("email");
    if (emailFromStorage) {
      setEmail(emailFromStorage);
    } else {
      console.error("Email not found in session storage");
    }
  }, []);


  useEffect(() => {
    async function fetchCourse() {
      try {
        const res = await fetch(`http://localhost:8000/courses/${course_id}?email=${email}`);
        const data = await res.json();
        console.log("Course data:", data);
        setCourse(data.course);
      } catch (error) {
        console.error("Failed to fetch course:", error);
      }
    }

    if (course_id && email) fetchCourse();
  }, [course_id, email]);

  if (!course) {
    return <div className="text-center py-10 text-gray-500">Loading course...</div>;
  }

  return (
    <div className="p-6 flex flex-col items-center">
      <div className="w-full max-w-3xl">
        <header className="mb-8 text-center">
          <h1 className="text-3xl font-bold text-gray-800">{course.course_name}</h1>
          <p className="text-sm text-gray-500">{course.course_code} - {course.course_semester}</p>
        </header>

        <div className="flex flex-col space-y-6">
          <div className="bg-white rounded-lg shadow-md p-6">
            <h2 className="text-xl font-semibold mb-4">Course Navigation</h2>
            <nav className="space-y-2">
              <a href={`/courses/${course.course_id}/modules`} className="block p-3 bg-blue-50 text-blue-700 rounded-md hover:bg-blue-100 transition">
                Modules
              </a>
              <a href={`/courses/${course.course_id}/assignments`} className="block p-3 bg-blue-50 text-blue-700 rounded-md hover:bg-blue-100 transition">
                Assignments
              </a>
            </nav>
          </div>

          <div className="bg-white rounded-lg shadow-md p-6">
            <h2 className="text-xl font-semibold mb-4">Course Information</h2>
            <div className="space-y-3">
              <p><span className="font-medium">Course ID:</span> {course.course_id}</p>
              <p><span className="font-medium">Created:</span> {new Date(course.course_created_at).toLocaleDateString()}</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default CoursePage;
