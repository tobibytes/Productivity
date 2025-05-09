"use client"

import { useRouter } from "next/navigation";

type AssignmentCardProps = {
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
  };
  
  const AssignmentCard = ({
    assignment_course_id,
    assignment_id,
    assignment_description,
    assignment_due_at,
    assignment_unlock_at,
    assignment_points_possible,
    assignment_grading_type,
    assignment_name,
    assignment_submission_types,
    assignment_has_submitted_submissions,
    assignment_updated_at,
  }: AssignmentCardProps) => {
    const router = useRouter();
    return (
      <div className="bg-white rounded-xl shadow p-5 border border-gray-200 hover:shadow-md transition">
        <div className="flex justify-between items-start mb-2">
          <div>
            <h3 className="text-lg font-semibold text-gray-800" onClick={() => router.push(`/courses/${assignment_course_id}/assignments/${assignment_id}`)}>{assignment_name}</h3>
            <p className="text-sm text-gray-500">Assignment ID: {assignment_id}</p>
          </div>
          <span
            className={`text-xs px-2 py-1 rounded-full font-medium ${
              assignment_has_submitted_submissions
                ? "bg-green-100 text-green-700"
                : "bg-yellow-100 text-yellow-700"
            }`}
          >
            {assignment_has_submitted_submissions ? "Submitted" : "Not Submitted"}
          </span>
        </div>
  
        <p className="text-sm text-gray-600 mb-3 line-clamp-3">
          {assignment_description
            ? assignment_description.replace(/(<([^>]+)>)/gi, "")
            : "No description available."}
        </p>
  
        <ul className="text-sm text-gray-600 space-y-1">
          <li>
            <span className="font-medium">Course ID:</span> {assignment_course_id}
          </li>
          <li>
            <span className="font-medium">Points:</span> {assignment_points_possible}
          </li>
          <li>
            <span className="font-medium">Grading Type:</span> {assignment_grading_type}
          </li>
          <li>
            <span className="font-medium">Submission Types:</span>{" "}
            {assignment_submission_types.join(", ")}
          </li>
          <li>
            <span className="font-medium">Due:</span>{" "}
            {assignment_due_at ? new Date(assignment_due_at).toLocaleString() : "No due date"}
          </li>
          <li>
            <span className="font-medium">Unlocks:</span>{" "}
            {assignment_unlock_at ? new Date(assignment_unlock_at).toLocaleString() : "Immediately"}
          </li>
          <li>
            <span className="font-medium">Last Updated:</span>{" "}
            {new Date(assignment_updated_at).toLocaleString()}
          </li>
        </ul>
      </div>
    );
  };
  
  export default AssignmentCard;