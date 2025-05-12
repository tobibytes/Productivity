"use client"

import { useEffect, useState } from "react";
import CourseCard from "@/components/CourseCard";

interface Course {
  course_id: number;
  course_account_id: number;
  course_name: string;
  course_code: string;
  course_uuid: string;
  course_created_at: string;
  course_semester: string;
}

const CoursesPage = () => {
  const [courses, setCourses] = useState<Course[]>([]);

  useEffect(() => {
    async function fetchCourses() {
      try {
        const email = sessionStorage.getItem("email");
        const res = await fetch(`${process.env.BACKEND_URL}/courses?email=${email}`);
        const data = await res.json();
        setCourses(data.courses || []);
      } catch (error) {
        console.error("Failed to fetch courses", error);
      }
    }

    fetchCourses();
  }, []);

  return (
    <div className="p-6 flex flex-wrap items-center space-y-6 gap-6 min-h-full">
      {courses.map((course) => (
        <div key={course.course_id} className="w-full max-w-md">
          <CourseCard {...course} />
        </div>
      ))}
      {courses.length === 0 && (
        <div className="w-full text-center py-10 text-gray-500">
          No courses available. Please check back later.
        </div>
      )}
    </div>
  );
};

export default CoursesPage;
