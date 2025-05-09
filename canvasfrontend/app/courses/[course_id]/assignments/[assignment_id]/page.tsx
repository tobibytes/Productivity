"use client";

import { useParams } from "next/navigation";
import { useEffect, useState } from "react";
import AssignmentCard from "@/components/AssignmentCard";

interface AssignmentData {
  assignment_course_id: string;
  assignment_id: string;
  assignment_description?: string;
  assignment_due_at?: string;
  assignment_unlock_at?: string;
  assignment_points_possible: number;
  assignment_grading_type: string;
  assignment_name: string;
  assignment_submission_types: string[];
  assignment_has_submitted_submissions: boolean;
  assignment_updated_at: string;
}

export default function AssignmentPage() {
  const { assignment_id, course_id } = useParams();
  const [assignment, setAssignment] = useState<AssignmentData | null>(null);

  useEffect(() => {
    async function fetchAssignment() {
      try {
        const res = await fetch(
          `http://localhost:8000/courses/${assignment?.assignment_course_id}/assignments/${assignment_id}`
        );
        const data = await res.json();
        setAssignment(data.assignment);
      } catch (err) {
        console.error("Failed to fetch assignment:", err);
      }
    }

    if (assignment_id && course_id) {
      fetchAssignment();
    }
  }, [assignment_id, course_id]);

  if (!assignment) {
    return <div className="text-center py-10 text-gray-500">Loading...</div>;
  }

  return (
    <div className="max-w-4xl mx-auto px-6 py-10">
      <h1 className="text-3xl font-bold text-gray-800 mb-6">
        {assignment.assignment_name}
      </h1>

      <div className="mb-6">
        <AssignmentCard {...assignment} />
      </div>

      <div className="bg-white rounded-xl p-6 shadow border border-gray-200">
        <h2 className="text-xl font-semibold text-gray-700 mb-4">Submit Assignment</h2>
        <p className="text-sm text-gray-600 mb-4">
          Ready to turn in your work? Click the button below to go to the submission page.
        </p>
        <a
          href={`/courses/${course_id}/assignments/${assignment_id}/submit`}
          className="inline-block px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 transition"
        >
          Go to Submission Page
        </a>
      </div>
    </div>
  );
}
