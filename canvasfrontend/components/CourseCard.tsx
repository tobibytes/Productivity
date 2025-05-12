"use client";

import { useRouter } from "next/navigation";

type CourseCardProps = {
  course_id: number;
  course_account_id: number;
  course_name: string;
  course_code: string;
  course_uuid: string;
  course_created_at: string;
  course_semester: string;
};

const CourseCard = ({
  course_id,
  course_account_id,
  course_name,
  course_code,
  course_uuid,
  course_created_at,
  course_semester,
}: CourseCardProps) => {
  const router = useRouter();
  const email = sessionStorage.getItem("email");
  return (
    <div className="h-full bg-white rounded-xl shadow p-5 hover:shadow-lg transition border border-gray-200 flex flex-col justify-between cursor-pointer" onClick={() => router.push(`/courses/${course_id}?email=${email}`)}>
      <div>
        <h2 className="text-xl font-semibold text-gray-800 mb-1">{course_name}</h2>
        <p className="text-sm text-gray-500 mb-2">
          <span className="font-medium">Code:</span> {course_code}
        </p>
        <div className="text-sm text-gray-600 space-y-1">
          <p><span className="font-medium">Course ID:</span> {course_id}</p>
          <p><span className="font-medium">Created:</span> {new Date(course_created_at).toLocaleDateString()}</p>
          <p><span className="font-medium">Semester:</span> {course_semester}</p>
        </div>
      </div>
    </div>
  );
};

export default CourseCard;