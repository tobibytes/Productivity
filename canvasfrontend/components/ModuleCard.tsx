"use client";

import { useRouter } from "next/navigation";

type ModuleCardProps = {
  module_course_id: string;
  module_id: string;
  module_name: string;
  module_completed_at: string | null;
  module_state: string; // e.g. 'locked', 'started', 'completed'
  module_prerequisite_ids: number[];
};

const ModuleCard = ({
  module_course_id,
  module_id,
  module_name,
  module_completed_at,
  module_state,
  module_prerequisite_ids,
}: ModuleCardProps) => {
  const stateColors: Record<string, string> = {
    completed: "bg-green-100 text-green-700",
    started: "bg-blue-100 text-blue-700",
    locked: "bg-gray-100 text-gray-500",
  };
  const router = useRouter()

  return (
    <div className="w-full min-h-[180px] bg-white border border-gray-200 rounded-xl shadow p-4 hover:shadow-md transition" onClick={() => router.push(`/courses/${module_course_id}/modules/${module_id}`)}>
      <div className="flex justify-between items-start mb-3">
        <div>
          <h3 className="text-lg font-semibold text-gray-800" onClick={() => router.push(`/courses/${module_course_id}/modules/${module_id}/moduleitems`)}>{module_name}</h3>
          <p className="text-sm text-gray-500">Module ID: {module_id}</p>
        </div>
        <span
          className={`text-xs px-2 py-1 rounded-full font-medium capitalize ${
            stateColors[module_state] || "bg-yellow-100 text-yellow-700"
          }`}
        >
          {module_state}
        </span>
      </div>

      <ul className="text-sm text-gray-600 space-y-1">
        <li>
          <span className="font-medium">Course ID:</span> {module_course_id}
        </li>
        <li>
          <span className="font-medium">Completed At:</span>{" "}
          {module_completed_at
            ? new Date(module_completed_at).toLocaleString()
            : "Not completed"}
        </li>
        <li>
          <span className="font-medium">Prerequisites:</span>{" "}
          {module_prerequisite_ids.length > 0
            ? module_prerequisite_ids.join(", ")
            : "None"}
        </li>
      </ul>
    </div>
  );
};

export default ModuleCard;