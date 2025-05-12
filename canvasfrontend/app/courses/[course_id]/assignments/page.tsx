"use client";

import { useParams } from "next/navigation";
import { useEffect, useState } from "react";
import AssignmentCard from "@/components/AssignmentCard";

interface Assignment {
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

export default function AssignmentsPage() {
  const { course_id } = useParams();
  const [assignments, setAssignments] = useState<Assignment[]>([]);

  useEffect(() => {
    async function fetchAssignments() {
      try {
        console.log("Fetching assignments for course ID:", course_id);
        const res = await fetch(`${process.env.BACKEND_URL}/courses/${course_id}/assignments`);
        const data = await res.json();
        setAssignments(data.assignments || []);
      } catch (error) {
        console.error("Failed to fetch assignments:", error);
      }
    }

    if (course_id) fetchAssignments();
  }, [course_id]);

  return (
    <div className="p-6 space-y-6 flex flex-wrap gap-4 justify-center">
      {assignments.map((assignment) => (
        <div key={assignment.assignment_id} className="w-full max-w-md">
          <AssignmentCard {...assignment} />
        </div>
      ))}
      {assignments.length === 0 && (
        <div className="w-full text-center py-10 text-gray-500">
          No assignments available for this course. Please check back later.
        </div>
      )}
    </div>
  );
}
